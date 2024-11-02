"""
В этом файле находятся функции для создания клавиатур (меню).
"""

import telebot

from model import course_to_teachers, user_votes

COURSES = "courses"
MY_MARKS = "my_marks"
RATINGS = "ratings"
SHOW_TEACHERS = "show_teachers"
SELECT_TEACHER = "select_teacher"
LIKE_TEACHER = "like_teacher"
GO_BACK = "go_back"
REMOVE_MARK = "remove_mark"

back_button = telebot.types.InlineKeyboardButton("[ Назад ]", callback_data=GO_BACK)


def create_reply_keyboard(buttons_titles: list[str]):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    keyboard.add(*(telebot.types.KeyboardButton(title) for title in buttons_titles))
    return keyboard


def create_inline_keyboard(buttons: list[tuple[str, str]], back):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for title, callback_data in buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(title, callback_data=callback_data))
    if back:
        keyboard.add(back_button)
    return keyboard


def get_teachers_menu(course_name: str, back):
    return create_inline_keyboard([
        (teacher.name, f"{SELECT_TEACHER}:{teacher.name}")
        for teacher in course_to_teachers[course_name]
    ], back)

def get_my_marks_menu(user_id: str, back):
    return create_inline_keyboard([
        (f"{teacher_name} - {'👍' if vote_value == 1 else '👎'}", f"{REMOVE_MARK}:{teacher_name}")
        for teacher_name, vote_value in user_votes.get_user_votes(user_id)
    ], back)


def get_teacher_like_menu(teacher_name: str, back):
    return create_inline_keyboard([
        ("👍", f"{LIKE_TEACHER}:{teacher_name}:1"),
        ("👎", f"{LIKE_TEACHER}:{teacher_name}:-1"),
        ("[ Назад ]", f"{LIKE_TEACHER}:{teacher_name}:0"),
    ], False)


main_menu = create_inline_keyboard([
    ("Поставить оценку", COURSES),
    ("Мои оценки", MY_MARKS),
    ("Рейтинг преподавателей", RATINGS)
], False)

courses_menu = create_inline_keyboard([
    (course_name, f"{SHOW_TEACHERS}:{course_name}")
    for course_name in course_to_teachers
], True)
