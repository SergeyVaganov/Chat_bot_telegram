import os
import pandas as pd
import fasttext
from tg_bot.utils import txt_preprocessing
import logging
from tg_bot.utils.questions_for_intent import list_questction


logger = logging.getLogger(__name__)


class ModelIntent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.model_name = "intent_classificator"
        if len(os.listdir('./tg_bot/models/Intent_classificator')) == 1:
            self.creator()
        self.model = fasttext.load_model('./tg_bot/models/intent_classificator/fast_model')
        logger.info("ModelIntent - загружена")

    def get_class(self, text):
        txt = txt_preprocessing.ru_preprocessing(text, False)
        predict = self.model.predict(txt, k=1)
        return predict[0][0][-1:]

    @classmethod
    def get_me(cls):
        return cls._instance

    @classmethod
    def creator(cls):
        logger.info("ModelIntent - обучение модели классификатора интентов")
        path = "./tg_bot/utils/"
        df_train = pd.read_csv(path + "intent_dataset_label0.csv")
        for i, q in enumerate(list_questction):
            df = pd.DataFrame(q * 1000, columns=['Content'])
            df['label'] = i + 1
            df_train = df_train.append(df)
        df_train['Content'] = df_train['Content'].apply(str)
        df_train['preprocess_Content'] = df_train['Content'].apply(
            lambda x: txt_preprocessing.ru_preprocessing(x, False))
        df_train['label'] = df_train['label'].apply(lambda x: '__label__' + str(x))
        df_train[['label', 'preprocess_Content']].to_csv(path + 'train_data_intent.txt', header=False, index=False, sep="\t")
        model = fasttext.train_supervised(input=path + 'train_data_intent.txt', epoch=20)
        model.save_model('./tg_bot/models/intent_classificator/fast_model')
        logger.info("ModelIntent - модель классификатора интентов обучена")
        return True

