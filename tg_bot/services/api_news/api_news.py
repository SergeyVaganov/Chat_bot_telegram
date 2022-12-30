import urllib.request
import json
import random
import logging
logger = logging.getLogger(__name__)


class ApiNews:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bot):
        if bot['config'].tg_bot.use_news:
            self.off = False
            token = bot['config'].tg_bot.token_news
            self.url = f"https://newsdata.io/api/1/news?country=ru&apikey={token}&category="
            self.category = {'здоровье': 'health', 'политика': 'politics'}
            logger.info('ApiNews - включен')
        else:
            self.off = True
            logger.info('ApiNews - не используется, выключен')

    def get_off(self):
        return self.off

    def pull_news(self, cat):
        if self.off:
            return None
        with urllib.request.urlopen(self.url + cat) as url:
            return json.load(url)

    def parse_news(self):
        if self.off:
            return None
        self.news = []
        for i, cat in self.category.items():
            json_ = self.pull_news(cat)
            for j in json_['results']:
                if len(str(j['description'])) > 1024:
                    short = '.'.join(j['description'][:1024].split(sep='.')[:-1])
                else:
                    short = str(j['description'])
                news = {'category': cat, 'title': j['title'], 'link': j['link'], 'disc': short, 'img': j['image_url']}
                self.news.append(news)
        logger.info("К https://newsdata.io/api/ подключён успешно")

    def get_random_news(self, cat):
        if self.off:
            return None
        result = []
        for new in self.news:
            if new['category'] == cat:
                result.append(new)
        if len(result) == 0:
            return None
        index = random.randint(0, len(result)-1)
        return result[index]

    @classmethod
    def get_me(cls):
        return cls._instance
