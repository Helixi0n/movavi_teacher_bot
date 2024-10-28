import telebot

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
ratings = {}
game_graphics = ["Диана Шульга",
                 "Арина Атаманова"]
web_design = ["Марина Ефремова"]
robots = ["Влада Кузнецова",
          "Кирилл Коваленко",
          "Арина Атаманова"]
coding = ["Арина Атаманова",
          "Кирилл Коваленко",
          "Игорь Гетто",
          "Максим Насонов",
          "Илья Козлобородов",
          "Евгений Ермаков",
          "Влада кузнецова",
          "Егор Чеглов"]


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    mark_btn = telebot.types.KeyboardButton("Поставить оценку")
    rating_btn = telebot.types.KeyboardButton("Рейтинг преподавателей")
    keyboard.add(mark_btn, rating_btn)
    bot.send_message(message.chat.id, "Привет! Поставь оценку преподу, пж", reply_markup=keyboard)


@bot.message_handler(regexp='Поставить оценку')
def mark(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_game_graphics = telebot.types.InlineKeyboardButton("Игровая графика", callback_data="Игровая графика")
    btn_web_design = telebot.types.InlineKeyboardButton("Дизайн сайтов", callback_data="Дизайн сайтов")
    btn_robots = telebot.types.InlineKeyboardButton("Робототехника", callback_data="Робототехника")
    btn_coding = telebot.types.InlineKeyboardButton("Программирование", callback_data="Программирование")
    keyboard.add(btn_game_graphics, btn_web_design, btn_robots, btn_coding)
    bot.send_message(message.chat.id, "Выбери предмет:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    keyboard = telebot.types.InlineKeyboardMarkup()
    if callback.data == "Игровая графика":
        for i in game_graphics:
            keyboard.add(telebot.types.InlineKeyboardButton(i, callback_data=i))
    elif callback.data == "Дизайн сайтов":
        for i in web_design:
            keyboard.add(telebot.types.InlineKeyboardButton(i, callback_data=i))
    elif callback.data == "Робототехника":
        for i in robots:
            keyboard.add(telebot.types.InlineKeyboardButton(i, callback_data=i))
    elif callback.data == "Программирование":
        for i in coding:
            keyboard.add(telebot.types.InlineKeyboardButton(i, callback_data=i))

    bot.send_message(callback.message.chat.id, "Выбери учителя", reply_markup=keyboard)


@bot.message_handler(regexp='Рейтинг преподавателей')
def rating(message):
    global ratings
    rtngs = sorted(ratings.items(), key=lambda item: item[1], reverse=True)
    bot.send_message(message.chat.id, f"Рейтинг:\n {rtngs}")


print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)
