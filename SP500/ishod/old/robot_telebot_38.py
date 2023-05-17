'''
    краткая инструкция к телеграмму
    1) создаем телеграм бота в телеграмме через BotFather
    BotFather дает нам токен нашего бота
    Наш бот появляется в нашем телеграмме - если надо нажать Start - жмем Start
    2) запускаем робота, не подсоединяемся - он в окне пишет f"Телеграм Бот НЕ проинициализирован"
    потому что токен не прописан в роботе
    3) Идем в Сервис - в строке Telegram Token вбиваем полученный токен от телеграмма
    Сохраняем. Так Наш робот узнает о телеграмме
    4) закрываем робот
    5) запускаем робот, не подсоединяемся - он в окне пишет f"Телеграм Бот ПРОинициализирован"
    Далее В самом телеграм-боте пишем "/start" - в ответ получаем "Ваш id = XXXXX"
    Всё телеграм-бот привязан к роботу, а робот привязан к телеграм-боту
    Можно подсоединяться - Коннект
    (для верности можно опять выключить и включить робота)
'''


import telebot  # telegram
from threading import Thread
import time


# телеграм
class TelegramBot(Thread):
    def __init__(self, interactive, token, id):
        Thread.__init__(self)
        self.i = 0
        self.flag_run_telegram = True
        self.flag_sent_telegram = False
        self.interactive = interactive
        self.flag_id = False
        self.id = id
        self.token = token
        self.flag_token_correct = False

        self.bot = telebot.TeleBot(self.token)  # '5702031284:AAH4lK4VgIH5hUdVg-7JJNMG7y3a5cSf2pw')
        try:
            print(f"Проверка бота-{self.interactive}: {self.bot.get_me()}")
            self.flag_token_correct = True
            # если проверка токена прошла успешна
            if self.interactive == "interactive":
                # Функция, обрабатывающая команду /start
                @self.bot.message_handler(commands=["start"])
                def start(m, res=False):
                    self.bot.send_message(m.chat.id, 'Я на связи.')
                    self.bot.send_message(m.chat.id, 'Ваш id = ' + str(m.chat.id))
                    self.flag_id = True
                    self.id = m.chat.id

                # Получение сообщений от юзера
                @self.bot.message_handler(content_types=["text"])
                def handle_text(message):
                    self.bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
                    self.id = message.chat.id
                    print(f"{self.interactive} id = {self.id}")
                    # if message.text == "id":
                    #     self.bot.send_message(message.chat.id, message.chat.id)
                    #     self.flag_id = True
                    #     self.id = message.chat.id
        except:
            print(f"Telegram-{self.interactive}: Токен не корректен ({token})")

    def send(self, text):
        try:  # 987861324
            self.bot.send_message(self.id, text)
            # self.bot.send_message(self.id, f"Коннект!!!! {self.i} {self.interactive}")
            # self.bot.send_message("", f"Салют!!!! {self.i} {self.interactive}")
        except:
            print(f"ID ({self.id}) не корректен. Введите корректный ID")

    def run(self):
        # проверяем есть ли у нас токен
        # while not self.flag_run_telegram:
        #
        #     time.sleep(0.5)

        # токена у нас нет - можно сразу завершить поток телеграмма

        print(f"Begin Telegram: {self.interactive}")

        # запуск интерактивного телеграм бота
        if self.interactive == "interactive":
            # self.bot.infinity_polling(long_polling_timeout=2)
            try:
                self.bot.polling(none_stop=True, interval=0, long_polling_timeout=1)  #
            except Exception as e:
                print(f"Ошибка в Telegram-{self.interactive}: {e}")
            # long_polling_timeout - это время - которое проходит между bot.stop_polling
            # и до выхода из bot.polling

        while self.flag_run_telegram:
            print(f"from Telegram-{self.interactive}: {self.i}")
            self.i += 1
            time.sleep(0.5)
            if self.flag_sent_telegram:
                self.flag_sent_telegram = False
                try:  # 987861324
                    self.bot.send_message(self.id, f"Коннект!!!! {self.i} {self.interactive}")
                    # self.bot.send_message("", f"Салют!!!! {self.i} {self.interactive}")
                except:
                    print(f"ID ({self.id}) не корректен. Введите корректный ID")

        print(f"Закрыли Телеграм-{self.interactive}")
