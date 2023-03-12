from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters

from .config import Config
from .utils import logger

def create_bot(config=Config):
    application = Application.builder().token(config.TOKEN).build()

    from .handlers import handle_button, handle_text
    from .jobs import start_notifications

    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(CallbackQueryHandler(handle_button))

    start_notifications(config, application)
    logger.info("bot created")
    return application
