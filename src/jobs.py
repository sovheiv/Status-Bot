from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes

from .config import Config


def start_notifications(config: Config, application: Application):
    application.job_queue.run_once(first_msg, user_id=config.ADMIN_ID, when=0, data=config.START_TIME)
    application.job_queue.run_repeating(
        update_time,
        interval=config.AUTOCHECK_INTERVAL,
        first=config.AUTOCHECK_INTERVAL,
        user_id=config.ADMIN_ID,
        data=config.START_TIME,
    )


async def first_msg(context: ContextTypes.DEFAULT_TYPE):
    resp = await context.bot.send_message(
        chat_id=context.job.user_id,
        text=f"Server started\n{context.job.data.strftime('%d/%m/%Y, %H:%M:%S')}",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )
    context.user_data["msg_id"] = resp.message_id


async def update_time(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.edit_message_text(
        f"Server was online\nfrom {context.job.data.strftime('%d/%m/%Y, %H:%M:%S')}\nto {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}",
        chat_id=context.job.user_id,
        message_id=context.user_data.get("msg_id"),
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )
