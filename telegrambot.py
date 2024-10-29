import os

import telebot
from dotenv import load_dotenv

from markup import create_inline_keyboard

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if not TOKEN:
    print("Переменная TELEGRAM_BOT_TOKEN не задана!")
    exit(-1)

bot = telebot.TeleBot(TOKEN)

main_menu = create_inline_keyboard([
    ("Поставить оценку", "courses"),
    ("Моя оценка", "my_marks"),
    ("Рейтинг преподавателей", "ratings")
])


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выбери действие",
        reply_markup=main_menu
    )


print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)
