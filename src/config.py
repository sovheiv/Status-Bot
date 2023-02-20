from environs import Env
from datetime import datetime

env = Env()
env.read_env(override=True)


class Config:
    TOKEN = env.str("TOKEN")
    ADMIN_ID = env.int("ADMIN_ID")
    AUTOCHECK_INTERVAL = env.int("AUTOCHECK_INTERVAL")
    START_TIME = datetime.now()
