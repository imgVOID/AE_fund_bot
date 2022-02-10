from os.path import abspath
from loader import config


# scheduled action, more information in the app.py file
async def scheduled_logs_clean(*args):
    apps = tuple(config.LOGGING_APPS.keys())
    levels = tuple(config.LOGGING_APPS.values())
    for i in range(0, len(apps)):
        open(abspath(f"data/logs/{apps[i]}/{levels[i]}.txt"), 'w').close()
