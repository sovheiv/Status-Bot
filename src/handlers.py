from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src import Config

from .utils import admin_required, handle_noedit, log


@log()
@handle_noedit()
@admin_required()
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()
    await context.bot.edit_message_text(
        f"Server was online\nfrom {Config.START_TIME.strftime(Config.DATETIME_FORMAT)}\nto {datetime.now().strftime(Config.DATETIME_FORMAT)}",
        update.message.chat_id,
        context.user_data.get("msg_id"),
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )


@log()
@handle_noedit()
@admin_required()
async def handle_button(update: Update, _) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        f"Server was online\nfrom {Config.START_TIME.strftime(Config.DATETIME_FORMAT)}\nto {datetime.now().strftime(Config.DATETIME_FORMAT)}",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Is online now?", callback_data="is_online")
        ),
    )
