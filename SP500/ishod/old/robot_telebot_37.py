import telebot  # telegram
from threading import Thread
import time


# телеграм
class TelegramBot(Thread):
    def __init__(self, interactive):
        Thread.__init__(self)
        self.i = 0
        self.flag_run_telegram = True
        self.flag_sent_telegram = False
        self.interactive = interactive


        self.bot = telebot.TeleBot('5702031284:AAH4lK4VgIH5hUdVg-7JJNMG7y3a5cSf2pw')

        try:
            self.bot.send_message(987861324, "Привет2!!!! " + self.interactive)
        except:
            print("ID не корректен. Введите корректный ID")

        if self.interactive == "interactive":
            # Функция, обрабатывающая команду /start
            @self.bot.message_handler(commands=["start"])
            def start(m, res=False):
                self.bot.send_message(m.chat.id, 'Я на связи.')
                self.bot.send_message(m.chat.id, 'Ваш id = ' + str(m.chat.id))

            # Получение сообщений от юзера
            @self.bot.message_handler(content_types=["text"])
            def handle_text(message):
                self.bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
                if message.text == "id":
                    self.bot.send_message(message.chat.id, message.chat.id)

    def run(self):
        # проверяем есть ли у нас токен
        while not self.flag_run_telegram:

            time.sleep(0.5)

        # токена у нас нет - можно сразу завершить поток телеграмма


        print(f"Begin Telegram: {self.interactive}")
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
                try:
                    self.bot.send_message(987861324, f"Салют!!!! {self.i} {self.interactive}")
                    # self.bot.send_message("", f"Салют!!!! {self.i} {self.interactive}")
                except:
                    print("ID не корректен. Введите корректный ID")

        print(f"Закрыли Телеграм-{self.interactive}")
