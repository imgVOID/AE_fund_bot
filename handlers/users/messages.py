from aiogram import types
from loader import dp, config


# Эхо хендлер, куда летят текстовые сообщения в бот, без указанного состояния
#@dp.message_handler(
#    lambda message: message.chat.type == 'private',
#)
#async def bot_echo(message: types.Message):
#    await message.answer(f"Эхо без состояния."
#                         f"Сообщение:\n"
#                         f"{message}")
