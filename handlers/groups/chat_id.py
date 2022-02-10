from aiogram.types import Message, ContentTypes
from loader import dp, config


@dp.message_handler(
    lambda message: message.from_user.id in config.admins,
    commands={'chat_id'}, content_types=ContentTypes.TEXT
)
async def get_chat_id(message: Message):
    if message.chat.id in config.groups:
        await message.reply(message.chat.id)
    else:
        await message.reply(
            "Пожалуйста, вызовите команду из чата нужной вам группы"
        )
