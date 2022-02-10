import logging

from aiogram import Dispatcher

from loader import config


async def on_startup_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
