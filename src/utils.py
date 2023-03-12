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

            logger.info(
                f"Handler: {handler.__name__}, {user.id} {user.username} {data}"
            )

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
                id = update.callback_query.from_user.id
            else:
                id = update.message.from_user.id

            if str(id) in Config.ADMIN_IDS:
                return await handler(update, context)
            logger.error("Unknown user")

        return wrapped

    return wrapper

def gen_report_text(start_time, dt_format):
    if not os.path.isfile("work_time.json"):
        return False

    with open("work_time.json", "r") as file:
        unix = json.load(file)["last_active_time"]
        last_time = datetime.fromtimestamp(unix)
    return f"Server was offline for {delta(start_time, last_time)}\nfrom {start_time.strftime(dt_format)}\nto {last_time.strftime(dt_format)}"


def delta(start_time: datetime, last_time: datetime):
    start_time -= timedelta(microseconds=start_time.microsecond)
    return str(start_time - last_time)