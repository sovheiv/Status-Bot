import json
import logging
import logging.config
import os
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

import yaml
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from src import Config

Path("logs").mkdir(parents=True, exist_ok=True)
with open("./logger.yaml", "r") as stream:
    logger_config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(logger_config)
logger = logging.getLogger(name="bot_logger")

os.makedirs(Config.TIME_DATA_PATH.split("/")[0], exist_ok=True,)


def log():
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.callback_query:
                user = update.callback_query.from_user
                data = f"callback: {update.callback_query.data}"
            else:
                user = update.message.from_user
                data = f"message: {update.message.text}"

            logger.info(f"Handler: {handler.__name__}, {user.id} {user.username} {data}")

            return await handler(update, context)

        return wrapped

    return wrapper


def handle_noedit():
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(*args, **kwargs):
            try:
                return await handler(*args, **kwargs)
            except BadRequest:
                logger.error(f"too frequent updates")

        return wrapped

    return wrapper


def admin_required():
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.callback_query:
                user_id = update.callback_query.from_user.id
            else:
                user_id = update.message.from_user.id

            if str(user_id) in Config.ADMIN_IDS:
                return await handler(update, context)
            logger.error("Unknown user")

        return wrapped

    return wrapper


def gen_report_text(start_time, dt_format):
    if not os.path.isfile(Config.TIME_DATA_PATH):
        return False

    with open(Config.TIME_DATA_PATH, "r") as file:
        unix = json.load(file)["last_active_time"]
        last_active_time = datetime.fromtimestamp(unix)
    return gen_msg(last_active_time, start_time, False)


def gen_msg(start_time: datetime, finish_time: datetime, online: bool = True):
    return f"""Server was {"on" if online else "off"}line for {delta(start_time, finish_time)}
from {start_time.strftime(Config.DATETIME_FORMAT)}
to {finish_time.strftime(Config.DATETIME_FORMAT)}"""


def delta(start_time: datetime, finish_time: datetime):
    start_time -= timedelta(microseconds=start_time.microsecond)
    finish_time -= timedelta(microseconds=finish_time.microsecond)
    return str(finish_time - start_time)
