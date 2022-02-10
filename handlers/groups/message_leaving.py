from aiogram.types import ContentTypes, Message
from loader import dp, db_async


@dp.message_handler(
    lambda message: message.chat.type == 'supergroup',
    content_types=ContentTypes.LEFT_CHAT_MEMBER
)
async def group_delete_member(message: Message):
    errors = await db_async.delete_user(message.chat.id, message.from_user.id, message.from_user.username)
    await message.reply('Ты удален!') if not errors else print(errors)
