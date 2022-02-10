import logging
import os
import shutil
from time import strftime
from file_read_backwards import FileReadBackwards


def setup_logging(level_name: str, logger_name):
    levels = {'debug': logging.DEBUG, 'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO}
    path = os.path.abspath(f"data/logs/{logger_name}/")
    filename = f"{level_name}.txt"
    if not os.path.exists(path):
        os.makedirs(path)
    scheduler_debug_log = logging.getLogger(logger_name)
    scheduler_debug_log.propagate = False
    try:
        file_handler = logging.FileHandler(filename=os.path.join(path, filename), encoding="utf-8")
        scheduler_debug_log.setLevel(levels[level_name])
    except KeyError:
        raise ValueError("Invalid logging level.")
    except Exception:
        raise Exception("Something went wrong.")
    scheduler_debug_log.addHandler(file_handler)
    return scheduler_debug_log


def check_job_logs(job_name: str, level_name: str):
    with FileReadBackwards(
            os.path.abspath(f"data/logs/apscheduler/{level_name}.txt"), encoding="utf-8"
    ) as log:
        for _ in range(21):
            line = log.readline()
            if job_name in line and strftime("%Y-%m-%d %H:") in line and "successfully" in line:
                return
    raise RuntimeWarning("Scheduled job's logs are missing") from BaseException


def delete_logs(app_name):
    shutil.rmtree(os.path.abspath(f"data/logs/{app_name}/"))


if __name__ == "__main__":
    check_job_logs("Minecraft News", "debug")
