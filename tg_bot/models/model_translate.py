import logging
import os
from transformers import FSMTForConditionalGeneration, FSMTTokenizer
logger = logging.getLogger(__name__)


class ModelTranslate:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.model_name = "facebook/wmt19-en-ru"
        if len(os.listdir('./tg_bot/models/translate')) == 1:
            self.tokenizer = FSMTTokenizer.from_pretrained(self.model_name)
            self.model = FSMTForConditionalGeneration.from_pretrained(self.model_name)
            self.model.save_pretrained('./tg_bot/models/translate/model')
            self.tokenizer.save_pretrained('./tg_bot/models/translate/tokenazer')
            logger.info("ModelTranslate - модель сохранена")
        else:
            self.tokenizer = FSMTTokenizer.from_pretrained('./tg_bot/models/translate/tokenazer')
            self.model = FSMTForConditionalGeneration.from_pretrained('./tg_bot/models/translate/model')
        logger.info("ModelTranslate - модель загружена")

    @classmethod
    def get_me(cls):
        return cls._instance

    async def tranlate(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded

