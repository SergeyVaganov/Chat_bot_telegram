import logging
import requests

logger = logging.getLogger(__name__)


class ApiNasa:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bot):
        if bot['config'].tg_bot.use_nasa:
            self.off = False
            token = bot['config'].tg_bot.token_nasa
            self.url = f'https://api.nasa.gov/planetary/apod?api_key={token}&count=1'
            logger.info('ApiNasa - включен')
        else:
            self.off = True
            logger.info('ApiNasa - не используется, выключен')

    def get_nasa(self):
        if self.off:
            return None
        response = requests.get(self.url)
        return response.json()

    @classmethod
    def get_me(cls):
        return cls._instance
