import json
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes
from telegram.error import BadRequest

from .config import Config
from .utils import handle_noedit, logger, gen_report_text, gen_msg


def start_notifications(config: Config, application: Application):
    report_text = gen_report_text(config.START_TIME, config.DATETIME_FORMAT)
    for id in config.ADMIN_IDS:
        if report_text:
            application.job_queue.run_once(
                report_shoutdown,
                user_id=id,
                when=0,
                data=report_text,
            )
        application.job_queue.run_once(
            first_msg,
            user_id=id,
            when=3,
            data={"START_TIME": config.START_TIME, "FORMAT": config.DATETIME_FORMAT},
        )
        application.job_queue.run_repeating(
            update_tg_time,
            interval=config.AUTOCHECK_INTERVAL,
            first=config.AUTOCHECK_INTERVAL,
            user_id=id,
            data={"START_TIME": config.START_TIME, "FORMAT": config.DATETIME_FORMAT},
        )

    application.job_queue.run_repeating(update_json_time, 1, 1)
    logger.info("notifications inited")


async def first_msg(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    resp = await context.bot.send_message(
        chat_id=context.job.user_id,
        text=f"Server started\nat: {data['START_TIME'].strftime(data['FORMAT'])}",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data=Config.CALLBACK)
        ),
    )
    context.user_data["msg_id"] = resp.message_id
    print(resp.message_id)
    await delete_prev_keyboard(context, resp.message_id)

    logger.info("first message sent")


async def delete_prev_keyboard(context: ContextTypes.DEFAULT_TYPE, message_id):
    for i in range(message_id - 4, message_id - 1):
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=context.job.user_id, message_id=i
            )
            logger.debug(f"{context.job.user_id} message {i} deleted")

        except BadRequest:
            logger.debug(f"{context.job.user_id} no message {i} to delete")


async def report_shoutdown(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.user_id, text=context.job.data, disable_notification=True
    )
    logger.info("report sent")


@handle_noedit()
async def update_tg_time(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    await context.bot.edit_message_text(
        gen_msg(data["START_TIME"], datetime.now()),
        chat_id=context.job.user_id,
        message_id=context.user_data.get("msg_id"),
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data=Config.CALLBACK)
        ),
    )
    logger.debug("tg time updated")


async def update_json_time(_):
    with open(Config.TIME_DATA_PATH, "w",) as file:
        json.dump({"last_active_time": int(datetime.now().timestamp())}, file)
