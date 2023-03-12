from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes

from .config import Config
from .utils import handle_noedit, logger


def start_notifications(config: Config, application: Application):
    for id in config.ADMIN_IDS:
        application.job_queue.run_once(
            first_msg,
            user_id=id,
            when=0,
            data={"START_TIME": config.START_TIME, "FORMAT": config.DATETIME_FORMAT},
        )
        application.job_queue.run_repeating(
            update_time,
            interval=config.AUTOCHECK_INTERVAL,
            first=config.AUTOCHECK_INTERVAL,
            user_id=id,
            data={"START_TIME": config.START_TIME, "FORMAT": config.DATETIME_FORMAT},
        )
    logger.info("notifications inited")


async def first_msg(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    resp = await context.bot.send_message(
        chat_id=context.job.user_id,
        text=f"Server started\nat: {data['START_TIME'].strftime(data['FORMAT'])}",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )
    context.user_data["msg_id"] = resp.message_id
    logger.info("first message sent")


@handle_noedit()
async def update_time(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    await context.bot.edit_message_text(
        f"Server was online\nfrom {data['START_TIME'].strftime(data['FORMAT'])}\nto {datetime.now().strftime(data['FORMAT'])}",
        chat_id=context.job.user_id,
        message_id=context.user_data.get("msg_id"),
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )
    logger.debug("msg time updated")
