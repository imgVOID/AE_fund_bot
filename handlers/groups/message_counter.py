from aiogram.types import ContentTypes, Message
from loader import dp, db, config


def increment_replies(message):
    try:
        original_author_signature = message.author_signature
    except (AttributeError, KeyError):
        original_author_signature = None
    try:
        forward_author = message.reply_to_message.from_user
    except (AttributeError, KeyError):
        pass
    else:
        try:
            author_signature = message.reply_to_message.author_signature
        except (AttributeError, KeyError):
            author_signature = None
            if forward_author.username:
                username = forward_author.username
            elif forward_author.first_name == '\u2063':
                username = 'Не указано'
            else:
                username = forward_author.first_name

            db.user_create(
                chat_id=message.chat.id, user_id=forward_author.id, username=username,
                signature=author_signature
            )
        else:
            db.user_create_signature(
                chat_id=message.chat.id, user_id=forward_author.id, signature=author_signature
            )

        db.increment_user_replies(
            chat_id=message.chat.id, user_id=forward_author.id, signature=message.reply_to_message.author_signature
        ) if forward_author.id != message.from_user.id or original_author_signature != author_signature else None


@dp.message_handler(
    lambda message: message.chat.id in config.groups and not message.from_user.is_bot,
    content_types=ContentTypes.TEXT
)
async def group_activity_counter(message: Message):
    username = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
    db.user_create(
        chat_id=message.chat.id, user_id=message.from_user.id, username=username
    )
    db.increment_user_messages(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    increment_replies(message=message)


@dp.message_handler(
    lambda message:
    message.chat.id in config.groups and message.from_user.is_bot and message.author_signature,
    content_types=ContentTypes.TEXT
)
async def group_activity_counter2(message: Message):
    db.user_create_signature(
        chat_id=message.chat.id, user_id=message.from_user.id, signature=message.author_signature
    )
    db.increment_user_messages(
        chat_id=message.chat.id, user_id=message.from_user.id, signature=message.author_signature
    )
    increment_replies(message=message)
