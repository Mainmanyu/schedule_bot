# bot.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN
from schedule import SCHEDULE

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Привет! Я бот вашей онлайн-школы. Нажмите на кнопку ниже, чтобы получить расписание уроков.",
        reply_markup=main_menu()
    )

# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Получить расписание", callback_data='get_schedule')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Обработка нажатий кнопок
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'get_schedule':
        schedule_message = generate_schedule_message()
        query.edit_message_text(text=schedule_message)

# Генерация сообщения с расписанием
def generate_schedule_message() -> str:
    message = "📚 Расписание уроков:\n\n"
    for day, lessons in SCHEDULE.items():
        message += f"**{day}:**\n" + "\n".join(lessons) + "\n\n"
    return message

def main():
    updater = Updater("TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
