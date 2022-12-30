from aiogram import types, Dispatcher
from tg_bot.filters.filter_intent import FilterIntentNewsPolitica, FilterIntentNewsHealth
import aiogram.utils.markdown as fmt


#     category ={'бизнес': 'business', 'развлечения':'entertainment',
#      'окружающая среда':'environment','еда':'food', 'здоровье':'health',
#      'политика':'politics', 'наука':'science', 'спорт':'sports', 'технологии':'technology',
#     'топ лучших':'top', 'в мире':'world'}


async def news_politica(message: types.Message, news):

    new = news.get_random_news('politics')
    if new is None or news.get_off():
        await message.answer('У меня пока нет новостей о политике')
    else:
        await message.answer(f"{fmt.hide_link(new['link'])}")


async def news_health(message: types.Message, news):
    new = news.get_random_news('health')
    if new is None or news.get_off():
        await message.answer('У меня пока нет новостей о медицине')
    else:
        await message.answer(f"{fmt.hide_link(new['link'])}")


def register_news(dp: Dispatcher):
    dp.register_message_handler(news_health, FilterIntentNewsHealth())
    dp.register_message_handler(news_politica, FilterIntentNewsPolitica())
