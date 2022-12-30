from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from tg_bot.models.model_dialog import ModelDialog
from tg_bot.models.model_translate import ModelTranslate
from tg_bot.models.model_summaryzer import ModelSummaryzer
from tg_bot.services.api_db.api_users import User
from tg_bot.services.api_news.api_news import ApiNews
from tg_bot.services.api_news.api_nasa import ApiNasa


class MiddlewareDialog(BaseMiddleware):

    async def setup_chat(self, data: dict, user: types.User):
        user_id = user.id
        user = User.create_or_get(user_id)
        data['user'] = user
        data['model'] = ModelDialog.get_me()
        data['news'] = ApiNews.get_me()
        data['nasa'] = ApiNasa.get_me()
        data['translate'] = ModelTranslate.get_me()
        data['summar'] = ModelSummaryzer.get_me()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)
