from os import sep
from data.hello_message import get_hello_message_group


class Globals:
    __slots__ = {
        "__BOT_TOKEN", "__ADMINS", "__CHANNELS", "__GROUPS", "__GROUPS_ALARM",
        "STATISTICS_MAIN_PATH", "HELLO_MESSAGE", "SCHEDULER_TIMINGS", "SCHEDULED_TASKS_IDS", "LOGGING_APPS",
    }

    def __init__(self, token, admins, channels, groups):
        self.__BOT_TOKEN = token
        self.__CHANNELS = tuple(channels)
        self.__ADMINS = tuple(int(admin_id) for admin_id in admins)
        self.__GROUPS = tuple(int(group_id) for group_id in groups)
        self.__GROUPS_ALARM = tuple(int(group_id) for group_id in groups)
        self.STATISTICS_MAIN_PATH = f'{sep.join(__file__.split(sep)[:-2])}/data/history_activity'
        self.HELLO_MESSAGE = get_hello_message_group()
        self.LOGGING_APPS = {"aiogram": "info", "apscheduler": "info"}
        self.SCHEDULER_TIMINGS = {
            "minecraft_news": {
                "name": "Minecraft News",
                "trigger": "interval",
                "datetime": {"hours": 0, "minutes": 0, "seconds": 1800}  # must be 30 minutes
            },
            "statistics_dump": {
                "name": "Statistics Dump",
                "trigger": "cron",
                "datetime": {"hour": 23, "minute": 50, "second": 20}  # must be everyday
            },
            "newsletter_fail": {
                "name": "Newsletter Check",
                "trigger": "interval",
                "datetime": {"hours": 0, "minutes": 30, "seconds": 15}  # must be 30 minutes
            },
            "logs_clean": {
                "name": "Logs Clean",
                "trigger": "cron",
                "datetime": {"hour": 23, "minute": 50, "second": 11}  # must be everyday
            }
        }
        self.SCHEDULED_TASKS_IDS = tuple(self.SCHEDULER_TIMINGS.keys())

    @property
    def token(self):
        return self.__BOT_TOKEN

    @property
    def admins(self):
        return self.__ADMINS

    @property
    def channels(self):
        return self.__CHANNELS

    @property
    def groups(self):
        return self.__GROUPS

    @property
    def groups_alarm(self):
        return self.__GROUPS_ALARM
