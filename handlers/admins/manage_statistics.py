from datetime import datetime, timedelta
from os.path import join
from io import BytesIO
from aiogram.types import Message, ContentTypes, MediaGroup, InputFile
from loader import dp, config, db


@dp.message_handler(
    lambda message: message.from_user.id in config.admins,
    commands={'statistics_today'}, content_types=ContentTypes.TEXT
)
async def get_statistics_dump_today(message: Message):
    date_time = (datetime.now().strftime("%d"), datetime.now().strftime("%m.%Y"))
    group_id = message.chat.id if message.chat.id in config.groups else message.get_args()
    group_id = config.groups[0] if not group_id and len(config.groups) == 1 else group_id
    try:
        data = db.get_activity_today(group_id)
    except ValueError as e:
        await message.reply(str(e))
    else:
        today_date = '.'.join(date_time)
        if len(data) < 3500:
            await message.reply(f"{today_date}\n<pre>{data}</pre>", parse_mode="html")
        else:
            await message.reply_document(InputFile(BytesIO(
                bytes(f"{today_date}\n{data}", encoding="utf-8"),
            )))


@dp.message_handler(
    lambda message: message.from_user.id in config.admins,
    commands={'statistics_yesterday'}, content_types=ContentTypes.TEXT
)
async def get_statistics_dump_yesterday(message: Message):
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    date_time = (yesterday.strftime('%m.%Y'), yesterday.strftime('%d'))
    media = MediaGroup()
    for group_id in config.groups:
        path = join(
            config.STATISTICS_MAIN_PATH, f"ID{group_id}",
            f"{date_time[0]}", f"Day {date_time[1]}.csv"
        )
        try:
            media.attach_document(document=InputFile(path_or_bytesio=path))
        except FileNotFoundError:
            await message.reply("Нет статистики за вчера.")
        else:
            await message.reply(f"Group ID: {group_id}")
            await message.reply_media_group(media=media)


@dp.message_handler(
    lambda message: message.from_user.id in config.admins,
    commands={'statistics_date'}, content_types=ContentTypes.TEXT
)
async def get_statistics_dump_date(message: Message):
    media = MediaGroup()
    arguments = message.get_args().split(" ")
    date = arguments.pop(0).split(".")
    try:
        if len(config.groups) == 1:
            group_id = config.groups[0]
        else:
            group_id = message.chat.id if message.chat.id in config.groups else arguments.pop(-1)
        path = join(
            config.STATISTICS_MAIN_PATH, f"ID{group_id}",
            f"{date[1]}.{date[2]}", f"Day {date[0]}.csv"
        )
        media.attach_document(document=InputFile(path_or_bytesio=path))
    except FileNotFoundError:
        await message.reply(f"За {'.'.join(arguments)} нет статистики.")
    except IndexError:
        await message.reply(f"Пожалуйста, введите дату в формате \"день.месяц.год\" и ID группы.")
    else:
        await message.reply_media_group(media=media)


# scheduled action, more information in the app.py file
async def save_statistics_dump(*args):
    date_time = (datetime.now().strftime("%m.%Y"), datetime.now().strftime("%d"))
    for group_id in config.groups:
        path = f'{config.STATISTICS_MAIN_PATH}/ID{group_id}/{date_time[0]}'
        db.backup_activity(group_id, path, date_time)
