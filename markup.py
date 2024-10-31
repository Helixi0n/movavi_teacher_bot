import telebot

from model import course_to_teachers, get_rating

COURSES = "courses"
MY_MARKS = "my_marks"
RATINGS = "ratings"
SHOW_TEACHERS = "show_teachers"
SELECT_TEACHER = "select_teacher"
LIKE_TEACHER = "like_teacher"


def create_reply_keyboard(buttons_titles: list[str]):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    keyboard.add(*(telebot.types.KeyboardButton(title) for title in buttons_titles))
    return keyboard


def create_inline_keyboard(buttons: list[tuple[str, str]]):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for title, callback_data in buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(title, callback_data=callback_data))
    return keyboard


def get_teachers_menu(course_name: str):
    return create_inline_keyboard([
        (teacher.name, f"{SELECT_TEACHER}:{teacher.name}")
        for teacher in course_to_teachers[course_name]
    ])

def get_teacher_like_menu(teacher_name: str):
    return create_inline_keyboard([
        ("👍", f"{LIKE_TEACHER}:{teacher_name}:1"),
        ("👎", f"{LIKE_TEACHER}:{teacher_name}:-1"),
    ])


main_menu = create_inline_keyboard([
    ("Поставить оценку", COURSES),
    ("Моя оценка", MY_MARKS),
    ("Рейтинг преподавателей", RATINGS)
])

courses_menu = create_inline_keyboard([
    (course_name, f"{SHOW_TEACHERS}:{course_name}")
    for course_name in course_to_teachers
])
