from aiogram import types, Dispatcher


async def dialog(message: types.Message, user, model):
    text = model.NLP_dialog(message.text, user.history[-10:])
    await message.answer(text)


def register_dialog(dp: Dispatcher):
    dp.register_message_handler(dialog)
