from aiogram.types import ContentTypes, Message
from loader import dp, db, config


@dp.message_handler(
    lambda message: message.chat.type == 'supergroup',
    content_types=ContentTypes.NEW_CHAT_MEMBERS
)
async def group_create_member(message: Message):
    errors = db.user_create(message.chat.id, message.from_user.id, message.from_user.username)
    await message.reply(config.HELLO_MESSAGE) if not errors else print(errors)
