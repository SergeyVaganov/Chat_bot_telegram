import logging
import os
from transformers import MBartTokenizer, MBartForConditionalGeneration
logger = logging.getLogger(__name__)


class ModelSummaryzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bot):
        if bot['config'].tg_bot.summaryzer_on:
            self.off = False
            self.model_name = "IlyaGusev/mbart_ru_sum_gazeta"
            if len(os.listdir('./tg_bot/models/summaryzer')) == 1:
                self.tokenizer = MBartTokenizer.from_pretrained(self.model_name)
                self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
                self.model.save_pretrained('./tg_bot/models/summaryzer/model')
                self.tokenizer.save_pretrained('./tg_bot/models/summaryzer/tokenazer')
                logger.info("ModelSummaryzer - модель сохранена")
            else:
                self.tokenizer = MBartTokenizer.from_pretrained('./tg_bot/models/summaryzer/tokenazer')
                self.model = MBartForConditionalGeneration.from_pretrained('./tg_bot/models/summaryzer/model')
            logger.info("ModelSummaryzer - модель загружена")
        else:
            self.off = True
            logger.info("ModelSummaryzer - Суммаризация выключена, модель не загружена")

    @classmethod
    def get_me(cls):
        return cls._instance

    def get_off(self):
        return self.off

    async def summar(self, text):
        if self.off:
            return None
        input_ids = self.tokenizer(
            [text],
            max_length=600,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
            )["input_ids"]
        output_ids = self.model.generate(
            input_ids=input_ids,
            no_repeat_ngram_size=4
            )[0]
        summary = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return summary

