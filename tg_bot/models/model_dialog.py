import os
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM

logger = logging.getLogger(__name__)

class ModelDialog:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.model_name = "sberbank-ai/rugpt3small_based_on_gpt2"
        # self.model_name = 'sberbank-ai/rugpt3large_based_on_gpt2'
        if len(os.listdir('./tg_bot/models/dialog')) ==1:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model.save_pretrained('./tg_bot/models/dialog/model')
            self.tokenizer.save_pretrained('./tg_bot/models/dialog/tokenazer')
            logger.info("ModelDialog - модель сохранена")
        else:
            self.tokenizer = AutoTokenizer.from_pretrained('./tg_bot/models/dialog/tokenazer')
            self.model = AutoModelForCausalLM.from_pretrained('./tg_bot/models/dialog/model')
        logger.info("ModelDialog - модель загружена")

    @classmethod
    def get_me(cls):
        return cls._instance

    def respond_to_dialog(self, texts):
        prefix = '\nx:'
        for i, t in enumerate(texts):
            prefix += t
            prefix += '\nx:' if i % 2 == 1 else '\ny:'
        tokens = self.tokenizer(prefix, return_tensors='pt')
        tokens = {k: v for k, v in tokens.items()}
        end_token_id = self.tokenizer.encode('\n')[0]
        size = tokens['input_ids'].shape[1]
        output = self.model.generate(
            **tokens,
            eos_token_id=end_token_id,
            do_sample=True,
            max_length=size+256,
            repetition_penalty=3.8,
            temperature=0.7,
            num_beams=3,
            length_penalty=0.01,
            pad_token_id= self.tokenizer.eos_token_id
            )
        decoded = self.tokenizer.decode(output[0])
        result = decoded[len(prefix):]
        return result.strip()

    def NLP_dialog(self, message, history):
        history.append(message)
        result = self.respond_to_dialog(history[-10:])
        history.append(result)
        return result

