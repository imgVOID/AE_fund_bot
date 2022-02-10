from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from environs import Env
from data.config import Globals
from utils.api_database_sync import SQLite
from utils.api_database_async import SQLiteAsync

ENV = Env()
ENV.read_env()
config = Globals(
    token=ENV.str("BOT_TOKEN"), admins=ENV.list("ADMINS"),
    groups=ENV.list("GROUPS"), channels=ENV.list("CHANNELS")
)
bot = Bot(
    token=config.token, parse_mode=types.ParseMode.HTML
)
storage = MemoryStorage()
scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
dp = Dispatcher(bot, storage=storage)
db = SQLite(name="activity", groups=config.groups)
db_async = SQLiteAsync()
