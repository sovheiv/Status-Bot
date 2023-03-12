import logging
import logging.config
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
