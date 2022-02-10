from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from data.hello_message import get_hello_message_bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(get_hello_message_bot().format(message.from_user.full_name))
