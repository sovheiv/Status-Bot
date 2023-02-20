import logging

from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters

from .config import Config
from .jobs import start_notifications

config = Config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def create_bot(config=config):
    application = Application.builder().token(config.TOKEN).build()

    from .handlers import handle_button, handle_text

    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(CallbackQueryHandler(handle_button))

    start_notifications(config, application)
    return application
