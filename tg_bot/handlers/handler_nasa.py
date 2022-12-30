from aiogram import types, Dispatcher
from tg_bot.filters.filter_intent import FilterIntentImageSpace
import aiogram.utils.markdown as fmt


async def foto_space(message: types.Message, nasa, translate, summar):

    new = nasa.get_nasa()
    if len(new) == 0 or new is None:
        await message.answer('У меня пока нет новых фото ')
    else:
        await message.answer(f"секундочку")
        ru_text = await translate.tranlate(new[0]['explanation'])
        text = ru_text if summar.get_off() else await summar.summar(ru_text)
        await message.answer(f"{fmt.hide_link(new[0]['url'])} {fmt.link(fmt.text(new[0]['date']), new[0]['hdurl'])} \n{text}")


def register_space(dp: Dispatcher):
    dp.register_message_handler(foto_space, FilterIntentImageSpace())
