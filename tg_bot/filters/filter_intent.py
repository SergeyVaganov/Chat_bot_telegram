from aiogram.dispatcher.filters import BoundFilter
from tg_bot.models.model_intent import ModelIntent
from aiogram import types


class FilterIntentNewsPolitica(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        model = ModelIntent.get_me()
        return model.get_class(message.text) == str(1)


class FilterIntentNewsHealth(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        model = ModelIntent.get_me()
        return model.get_class(message.text) == str(2)


class FilterIntentImageSpace(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        model = ModelIntent.get_me()
        return model.get_class(message.text) == str(3)
