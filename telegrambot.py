import os

import telebot
from dotenv import load_dotenv

import markup
from model import teachers, find_teachers

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if not TOKEN:
    print("Переменная TELEGRAM_BOT_TOKEN не задана!")
    exit(-1)

bot = telebot.TeleBot(TOKEN)

FOTO_PATH = "Teachers_Photo/"

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выбери действие",
        reply_markup=markup.main_menu
    )


@bot.callback_query_handler(func=lambda callback: callback.data == markup.COURSES)
def handle_callback_courses(callback):
    bot.send_message(
        callback.message.chat.id,
        "Выбери курс",
        reply_markup=markup.courses_menu
    )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(markup.SHOW_TEACHERS))
def handle_callback_show_teachers(callback):
    course_name = callback.data.split(":")[1]
    bot.send_message(
        callback.message.chat.id,
        "Выбери учителя",
        reply_markup=markup.get_teachers_menu(course_name)
    )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(markup.SELECT_TEACHER))
def handle_callback_select_teacher(callback):
    teacher_name = callback.data.split(":")[1]
    teacher = find_teachers([teacher_name])[0]
    with open(FOTO_PATH + teacher.photo, "rb") as photo:
        bot.send_photo(
            callback.message.chat.id,
            photo=photo,
            caption=f"{teacher.name}\n{teacher.bio}",
            reply_markup=markup.get_teacher_like_menu(teacher_name)
        )


print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)
