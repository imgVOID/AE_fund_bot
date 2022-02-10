import logging
from time import strftime
from aiogram import Dispatcher

from loader import config
from utils.scripts_logging import check_job_logs


async def on_startup_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(admin, "Бот запущен")
        except Exception as err:
            logging.exception(err)


async def on_newsletter_fail_notify(dp: Dispatcher):
    job_config = config.SCHEDULER_TIMINGS[config.SCHEDULED_TASKS_IDS[0]]
    try:
        check_job_logs(job_name=job_config["name"], level_name=config.LOGGING_APPS["apscheduler"])
    except RuntimeWarning:
        print("Newsletter have been stopped")
        for admin in config.admins:
            try:
                await dp.bot.send_message(admin, "Не работает рассылка Minecraft!")
            except Exception as err:
                logging.exception(err)
    else:
        print(f"Newsletter is OK at {strftime('%Y-%m-%d %H:%M:%S')}")
