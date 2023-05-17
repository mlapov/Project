# @robot_sp_demo_bot
# token = 5702031284:AAH4lK4VgIH5hUdVg-7JJNMG7y3a5cSf2pw
# id  = 987861324
# pip install pytelegrambotapi

import telebot

# Создаем экземпляр бота
bot = telebot.TeleBot('5702031284:AAH4lK4VgIH5hUdVg-7JJNMG7y3a5cSf2pw')

try:
    bot.send_message("987861324", "Привет!!!!")
     # bot.send_message('@mlapov', "Привет!!!!")
except:
    print("ID не кор#ректен. Введите корректный ID")

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи.')
    bot.send_message(m.chat.id, 'Ваш id = ' + str(m.chat.id))


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
    if message.text == "id":
        bot.send_message(message.chat.id, message.chat.id)


# Запускаем бота
# bot.polling(none_stop=True, interval=0)



bot.infinity_polling()
