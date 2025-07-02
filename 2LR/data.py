import telebot
from datetime import datetime

token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Enter 'date', or 'time'.")

@bot.message_handler(func=lambda message: True)
def message(message):
    text = message.text.strip().lower()
    now = datetime.now()

    if text == 'date':
        date_str = now.strftime("%d.%m.%Y")
        bot.reply_to(message, f"Now: {date_str}")
    elif text == 'time':
        time_str = now.strftime("%H:%M:%S")
        bot.reply_to(message, f"Now: {time_str}")
    else:
        bot.reply_to(message, "No-no-no, enter date or time")

if __name__ == '__main__':
    bot.polling()
