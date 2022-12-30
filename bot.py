# может расширить число интентов
# писать рид ми
# логи выровнять
import asyncio
import logging
from aiogram import Bot, Dispatcher
from tg_bot.models.model_dialog import ModelDialog
from tg_bot.models.model_intent import ModelIntent
from tg_bot.models.model_translate import ModelTranslate
from tg_bot.models.model_summaryzer import ModelSummaryzer
from tg_bot.config import load_config
from tg_bot.filters.filter_intent import FilterIntentNewsPolitica, FilterIntentNewsHealth,FilterIntentImageSpace
from tg_bot.handlers.handler_dialog import register_dialog
from tg_bot.handlers.hendler_news import register_news
from tg_bot.handlers.handler_nasa import  register_space
from tg_bot.middlewares.middleware_dialog import MiddlewareDialog
from tg_bot.services.api_news.api_news import ApiNews
from tg_bot.services.api_news.api_nasa import ApiNasa


logger = logging.getLogger(__name__)

def register_all_middlewares(dp):
    dp.setup_middleware(MiddlewareDialog())

def register_all_filters(dp):
    dp.filters_factory.bind(FilterIntentNewsPolitica)
    dp.filters_factory.bind(FilterIntentNewsHealth)
    dp.filters_factory.bind(FilterIntentImageSpace)

def register_all_handlers(dp):
    register_news(dp)
    register_space(dp)
    register_dialog(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Старт бота")
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot)

    bot['config'] = config

    _ = ModelDialog()
    _ = ModelIntent()
    _ = ModelTranslate()
    _ = ModelSummaryzer(bot)
    news = ApiNews(bot)
    news.parse_news()
    _ = ApiNasa(bot)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot остановлен!")