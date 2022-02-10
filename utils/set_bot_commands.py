from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("statistics_today", "Получение статистики за сегодня"),
            types.BotCommand("statistics_yesterday", "Получение статистики за вчера"),
            types.BotCommand(
                "statistics_date",
                "Получение статистики по дате, укажите дату (формат 01.01.2021) и (опционально) ID группы"
            ),
            types.BotCommand("chat_id", "Получение ID группы, доступно из чата группы"),
            types.BotCommand("logs_today", "Получение файлов с логами бота, НЕ запускается из чата группы")
        ]
    )
