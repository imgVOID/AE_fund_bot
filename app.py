import logging
import websockets
import asyncio
from aiogram import executor
from loader import dp, scheduler, config
from handlers.groups.scheduled_newsletter_minecraft import get_minecraft_info
from handlers.admins.notify_admins import on_startup_notify, on_newsletter_fail_notify
from handlers.admins.scheduled_logs_deletion import scheduled_logs_clean
from handlers.admins.scheduled_statistics_backup import save_statistics_dump
from utils.set_bot_commands import set_default_commands
from utils.scripts_logging import setup_logging
from sockets.websocket_server import websocket_server_start


def schedule_jobs():
    minecraft_news = config.SCHEDULER_TIMINGS[config.SCHEDULED_TASKS_IDS[0]]
    statistics_dump = config.SCHEDULER_TIMINGS[config.SCHEDULED_TASKS_IDS[1]]
    newsletter_check = config.SCHEDULER_TIMINGS[config.SCHEDULED_TASKS_IDS[2]]
    logs_clean = config.SCHEDULER_TIMINGS[config.SCHEDULED_TASKS_IDS[3]]

    scheduler.add_job(
        get_minecraft_info, minecraft_news["trigger"], **minecraft_news["datetime"],
        id="minecraft_news", name=minecraft_news["name"], args=(dp,)
    )
    scheduler.add_job(
        save_statistics_dump, statistics_dump["trigger"], **statistics_dump["datetime"],
        id="statistics_dump", name=statistics_dump["name"], args=(dp,)
    )
    scheduler.add_job(
        on_newsletter_fail_notify, newsletter_check["trigger"], **newsletter_check["datetime"],
        id="newsletter_check", name=newsletter_check["name"], args=(dp,)
    )
    scheduler.add_job(
        scheduled_logs_clean, logs_clean["trigger"], **logs_clean["datetime"],
        id="logs_clean", name=logs_clean["name"], args=(dp,)
    )


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    schedule_jobs()


if __name__ == '__main__':
    print("Bot have been started, please look on the logs section")
    try:
        setup_logging(config.LOGGING_APPS['aiogram'], 'aiogram')
        setup_logging(config.LOGGING_APPS['apscheduler'], 'apscheduler')
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(websocket_server_start, '0.0.0.0', 8765)
        )
        scheduler.start()
        executor.start_polling(dp, on_startup=on_startup)

    except Exception as e:
        logging.exception(e)
