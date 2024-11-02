"""
Основной файл проекта.
Тут находятся только хендлеры.
"""

import os
from collections import defaultdict

import telebot
from dotenv import load_dotenv

import markup
from model import teachers, user_votes, get_rating

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if not TOKEN:
    print("Переменная TELEGRAM_BOT_TOKEN не задана!")
    exit(-1)

bot = telebot.TeleBot(TOKEN)

FOTO_PATH = "Teachers_Photo/"

back_stack = defaultdict(list)


@bot.message_handler(commands=['start'])
def handle_start(message):
    message = bot.send_message(
        message.chat.id,
        "Привет! Выбери действие",
        reply_markup=markup.main_menu
    )
    back_stack[message.chat.id].append(lambda: handle_start_replace(message))


def handle_start_replace(message):
    back_stack[message.chat.id].append(lambda: handle_start_replace(message))
    bot.edit_message_text(
        "Выбери действие",
        message.chat.id,
        message.message_id,
        reply_markup=markup.main_menu
    )


@bot.callback_query_handler(func=lambda callback: callback.data == markup.COURSES)
def handle_callback_courses(callback):
    back_stack[callback.message.chat.id].append(lambda: handle_callback_courses(callback))
    bot.edit_message_text(
        "Выбери курс",
        callback.message.chat.id,
        callback.message.id,
        reply_markup=markup.courses_menu
    )


@bot.callback_query_handler(func=lambda callback: callback.data == markup.RATINGS)
def handle_callback_rating(callback):
    back_stack[callback.message.chat.id].append(lambda: handle_callback_rating(callback))
    ratings = get_rating()
    res = "\n".join([
        f"{i + 1:>3}\. {teacher:<20} {rating}"
        for i, (teacher, rating) in enumerate(ratings)
    ])

    bot.edit_message_text(
        "*Топ\-10 преподавателей*:\n```" + res + "\n```",
        callback.message.chat.id,
        callback.message.id,
        parse_mode="MarkdownV2",
        reply_markup=markup.create_inline_keyboard([], True)
    )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(markup.SHOW_TEACHERS))
def handle_callback_show_teachers(callback):
    back_stack[callback.message.chat.id].append(lambda: handle_callback_show_teachers(callback))
    course_name = callback.data.split(":")[1]
    bot.edit_message_text(
        "Выбери учителя",
        callback.message.chat.id,
        callback.message.id,
        reply_markup=markup.get_teachers_menu(course_name, True)
    )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(markup.SELECT_TEACHER))
def handle_callback_select_teacher(callback):
    teacher_name = callback.data.split(":")[1]
    teacher = teachers.get_teachers([teacher_name])[0]
    with open(FOTO_PATH + teacher.photo, "rb") as photo:
        bot.send_photo(
            callback.message.chat.id,
            photo=photo,
            caption=f"{teacher.name}\n{teacher.bio}",
            reply_markup=markup.get_teacher_like_menu(teacher_name, False)
        )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(markup.LIKE_TEACHER))
def handle_callback_add_like(callback):
    _, teacher, vote_value = callback.data.split(":")
    vote_value = int(vote_value)
    if vote_value:
        user_votes.add_vote(callback.from_user.id, teacher, vote_value)
        bot.send_message(
            callback.message.chat.id,
            f"{teacher} получил от вас {'👍' if vote_value == 1 else '👎'}",
        )
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
    )


@bot.callback_query_handler(func=lambda callback: callback.data == markup.GO_BACK)
def handle_callback_go_back(callback):
    stack = back_stack[callback.message.chat.id]
    if stack:
        stack.pop()
        stack.pop()()


print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)
