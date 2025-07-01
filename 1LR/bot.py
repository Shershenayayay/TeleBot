import telebot
import config \\ Хранит токен

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"]) 
def repeat(message): \\ Функция repeat будет работать после любого текстового сообщения
    bot.send_message(message.chat.id, message.text) \\ Отправляет обратно в чат то же самое сообщение

if __name__ == '__main__': \\ Проверка запуска скрипта напрямую
    bot.infinity_polling() \\ Запускает постоянный цикл проверки входящих сообщений