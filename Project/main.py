import telebot
from telebot import types
from statistics import mean, median, variance, stdev, multimode
from Support import supp, answer
import random

bot = telebot.TeleBot('')

# Данные и состояние пользователя
user_data = {}
user_state = {}  # 'waiting_for_numbers', 'waiting_for_operation'

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Здравствуйте, {user_name}! Для начала я вас попрошу ввести ряд чисел. Это будет не трудно?")
    bot.send_message(message.chat.id, "И кстати, если вам вздумается работать над иным рядом чисел, то просто введите команду \start после работы над прежним")

    bot.send_message(message.chat.id, "Также оповещаюю о том, что по случае вашего желания, вы можете ознакомиться с контактами разработки.")
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Красивый человек", url = "https://t.me/Shershenayayay")
    markup.add(button)
    bot.send_message(message.chat.id, "Разработчик:", reply_markup=markup)
    
    user_state[message.chat.id] = 'waiting_for_numbers'
    user_data[message.chat.id] = None  # Очистка предыдущих данных

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if state == 'waiting_for_numbers':
        try:
            raw_input = message.text.replace(',', ' ')
            numbers = list(map(float, raw_input.split()))
            if not numbers:
                raise ValueError
            user_data[chat_id] = numbers
            user_state[chat_id] = 'waiting_for_operation'
            
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                "Отсортировать",
                "Дисперсия",
                "Среднее выборочное",
                "Среднеквадратическое отклонение",
                "Мода",
                "Медиана",
                "Помощь"
            ]
            keyboard_rows = []
            for btn in range(0, len(buttons), 2):
                row = []
                row = buttons[btn:btn+2]  # срез из двух элементов
                keyboard_rows.append(row)
                markup.keyboard = keyboard_rows

            bot.send_message(chat_id, "Что же, далее вам следует выбрать одну из представленных операций:", reply_markup=markup)
        except ValueError:
            bot.send_message(chat_id, "Я вам заявляю, что вы где-то допустили ошибку. Введите ряд чисел заново и не забывайте про правила.")

    elif state == 'waiting_for_operation':
        numbers = user_data.get(chat_id)
        if not numbers:
            bot.send_message(chat_id, "А вы уверены, что вы правы? Попробуйте пожалуйста заново ввести числа.")
            user_state[chat_id] = 'waiting_for_numbers'
            return

        text = message.text

        try:
            if text == "Отсортировать":
                sorted_numbers = sorted(numbers)
                bot.send_message(chat_id, f"Не без труда отсортированный ряд: {sorted_numbers}")

            elif text == "Дисперсия":
                if len(numbers) < 2:
                    bot.send_message(chat_id, "А вы знали, что для вычисления дисперии необходима для минимума пара чисел? Теперь вы это знаете.")
                    return
                disp = variance(numbers)
                bot.send_message(chat_id, f"По исполнении доставлено: {disp}")

            elif text == "Среднее выборочное":
                avg = mean(numbers)
                bot.send_message(chat_id, f"Среднее выборочное, оно же Xв, оно же для кого-то мат. ожидание: {avg}")

            elif text == "Среднеквадратическое отклонение":
                if len(numbers) < 2:
                    bot.send_message(chat_id, "Сделаю ещё одно для вас открытие. Для СКО необходима для минимума пара чисел.")
                    return
                std_dev = stdev(numbers)
                bot.send_message(chat_id, f"Пожалуйста: {std_dev}")

            elif text == "Мода":
                modes = multimode(numbers)
                if len(modes) == len(set(numbers)):
                    bot.send_message(chat_id, "Да, так сложилось, что все числа одинаково разные.")
                else:
                    bot.send_message(chat_id, f"Мода(ы): {modes}")

            elif text == "Медиана":
                med = median(numbers)
                bot.send_message(chat_id, f"Медиана: {med}")
            
            elif text == "Помощь":
                bot.send_message(chat_id, random.choice(list(supp)))

            else:
                bot.send_message(chat_id, "Пожалуйста, выберите операцию из предложенных.")

        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {e}")

        # Оставляем состояние для дальнейших операций с тем же рядом
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "Отсортировать",
            "Дисперсия",
            "Среднее выборочное",
            "Среднеквадратическое отклонение",
            "Мода",
            "Медиана",
            "Помощь"
        ]
        keyboard_rows = []
        for btn in range(0, len(buttons), 2):
            row = []
            row = buttons[btn:btn+2]  # срез из двух элементов
            keyboard_rows.append(row)
            markup.keyboard = keyboard_rows

        bot.send_message(
            chat_id,
            random.choice(list(answer)),
            reply_markup=markup
        )

bot.polling()
