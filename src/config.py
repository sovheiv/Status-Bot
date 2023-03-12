from environs import Env
from datetime import datetime

env = Env()
env.read_env(override=True)

print("load conf")
class Config:
    TOKEN = env.str("TOKEN")
    ADMIN_ID = env.str("ADMIN_ID")
    ADMIN_IDS = env.list("ADMIN_IDS")
    AUTOCHECK_INTERVAL = env.int("AUTOCHECK_INTERVAL")
    DATETIME_FORMAT = env.str("DATETIME_FORMAT")
    START_TIME = datetime.now()
