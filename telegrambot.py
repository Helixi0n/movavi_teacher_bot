import telebot
from telebot.types import ReplyKeyboardRemove

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
    commands = ["Поставить оценку", "Рейтинг преподавателей"]
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(command) for command in commands]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "Привет! Поставь оценку преподу, пж")
    bot.register_next_step_handler(message, choice)

def choice(message):
    txt = message.text
    if txt == "Поставить оценку":
        bot.register_next_step_handler(message, mark)
    elif txt == "Рейтинг преподавателей":
        bot.register_next_step_handler(message, rating)
    else:
        bot.send_message(message.chat.id, "Чё?")

def mark(message):
    pass 

def rating(message):
    ratings = sorted(ratings.items, key=lambda x: -x[1])
    bot.send_message(message.chat.id, f"Рейтинг:\n{raitings}")


keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [telebot.types.KeyboardButton(good) for good in goods]
keyboard.add(*buttons)


print("Сервер запущен.")
bot.polling(
    non_stop=True,
    interval=1
)

#fdjfdjfksk