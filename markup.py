import telebot

def create_reply_keyboard(buttons_titles: list[str]):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    keyboard.add(*(telebot.types.KeyboardButton(title) for title in buttons_titles))
    return keyboard


def create_inline_keyboard(buttons: list[tuple[str,str]]):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for title, callback_data in buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(title, callback_data=callback_data))
    return keyboard


