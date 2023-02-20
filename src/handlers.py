from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from src import config, logger


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if update.message.from_user.id == config.ADMIN_ID:
        await update.message.delete()
        logger.info(f"User: {user.username}: {update.message.text}")

        try:
            await context.bot.edit_message_text(
                f"Server was online\nfrom {config.START_TIME.strftime('%d/%m/%Y, %H:%M:%S')}\nto {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}",
                update.message.chat_id,
                context.user_data.get("msg_id"),
                reply_markup=InlineKeyboardMarkup.from_button(
                    InlineKeyboardButton("Is online now?", callback_data="is_online")
                ),
            )
        except BadRequest:
            logger.error(f"too frequent updates")
    else:
        logger.info(f"Unknown user: {user.username} {user.id}")


async def handle_button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text(
            f"Server was online\nfrom {config.START_TIME.strftime('%d/%m/%Y, %H:%M:%S')}\nto {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton("Is online now?", callback_data="is_online")
            ),
        )
    except BadRequest:
        logger.error(f"too frequent updates")
