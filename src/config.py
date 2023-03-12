from datetime import datetime

from environs import Env

env = Env()
env.read_env(override=True)


class Config:
    TOKEN = env.str("TOKEN")
    ADMIN_IDS = env.list("ADMIN_IDS")
    AUTOCHECK_INTERVAL = env.int("AUTOCHECK_INTERVAL")
    DATETIME_FORMAT = env.str("DATETIME_FORMAT")
    TIME_DATA_PATH = env.str("TIME_DATA_PATH")
    START_TIME = datetime.now()
    CALLBACK = f"is_online_{int(START_TIME.timestamp())}"
