from os.path import abspath
from aiogram.types import Message, ContentTypes, InputFile, MediaGroup
from loader import dp, config


@dp.message_handler(
    lambda message: message.from_user.id in config.admins and message.chat.id not in config.groups,
    commands={'logs_today'}, content_types=ContentTypes.TEXT
)
async def get_logs_today(message: Message):
    apps = tuple(config.LOGGING_APPS.keys())
    levels = tuple(config.LOGGING_APPS.values())
    log_files = []
    media = MediaGroup()
    for i in range(0, len(apps)):
        try:
            log_files.append(InputFile(abspath(f"data/logs/{apps[i]}/{levels[i]}.txt")))
            media.attach_document(log_files[-1])
        except FileNotFoundError:
            pass
    try:
        await message.reply_media_group(media)
    except Exception as e:
        await message.reply(str(e))
