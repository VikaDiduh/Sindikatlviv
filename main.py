import os
import logging

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Привіт", callback_data='hello')],
        [InlineKeyboardButton("Вітання", callback_data='greetings')],
        [InlineKeyboardButton("Автор", callback_data='author')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Виберіть опцію:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'hello':
        await query.message.reply_text(f'хаю хай {update.effective_user.first_name}')
    elif query.data == 'greetings':
        await query.message.reply_text(f'Привіт, {update.effective_user.first_name}!')
    elif query.data == 'author':
        await query.message.reply_text(f'Цього бота створив Дідух Вікторія')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    messege = update.message.text.lower()

    if 'привіт' in messege:
        reply_text = f'привіт {update.effective_user.first_name}!'
    elif 'гудбай' in messege:
        last_name = update.effective_user.last_name
        if last_name is None:
            reply_text = f'допобачення {update.effective_user.first_name}!'
        else:
            reply_text = f'допобачення {update.effective_user.first_name} {last_name}!'
    else:
        reply_text = 'Я тебе не розумію '

    keyboard = [
        [InlineKeyboardButton("Привіт", callback_data='hello')],
        [InlineKeyboardButton("Вітання", callback_data='greetings')],
        [InlineKeyboardButton("Автор", callback_data='author')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(reply_text, reply_markup=reply_markup)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()