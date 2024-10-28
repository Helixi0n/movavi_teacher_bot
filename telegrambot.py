import telebot

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
ratings = {}
teacher = {
    "Программирование": ["Арина Атаманова", 
                         "Кирилл Коваленко", 
                         "Игорь Гетто", 
                         "Максим Насонов", 
                         "Илья Козлобородов", 
                         "Евгений Ермаков", 
                         "Влада кузнецова", 
                         "Егор Чеглов"],
    "Игровая графика": ["Диана Шульга", 
                        "Арина Атаманова"],
    "Дизайн сайтов": ["Марина Ефремова"],
    "Робототехника": ["Влада Кузнецова", 
                      "Кирилл Коваленко", 
                      "Арина Атаманова"]
    }

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_btn = telebot.types.KeyboardButton("Поставить оценку")
    rating_btn = telebot.types.KeyboardButton("Рейтинг преподавателей")
    keyboard.add(mark_btn, rating_btn)
    bot.send_message(message.chat.id, "Привет! Поставь оценку преподу, пж", reply_markup=keyboard)

@bot.message_handler(regexp='Поставить оценку')
def mark(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = [telebot.types.KeyboardButton(i) for i in teacher.keys()]
    keyboard.add(buttons)
    bot.send_message(message.chat.id, "Выбери предмет, учителя которого ты хочешь оценить", reply_markup=keyboard)

@bot.message_handler(regexp='Рейтинг преподавателей')
def rating(message):
    global ratings
    ratings = sorted(ratings.items, key=lambda item: -item[1])
    bot.send_message(message.chat.id, f"Рейтинг:\n {ratings}")



print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)
