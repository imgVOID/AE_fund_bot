from time import strftime
from datetime import datetime
from loader import config, db


# scheduled action, more information in the app.py file
async def save_statistics_dump(*args):
    date_time = (datetime.now().strftime("%m.%Y"), datetime.now().strftime("%d"))
    for group_id in config.groups:
        path = f'{config.STATISTICS_MAIN_PATH}/ID{group_id}/{date_time[0]}'
        db.backup_activity(group_id, path, date_time)
