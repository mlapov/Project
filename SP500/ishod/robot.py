"""
работает подсоединение с сервером
коннект и доисконнект корректны
Пара =  файл robot_5 + Interface_5

!!! КОНФИГУРАЦИЯ !!!!!!!!!!!!!!!!!!!!!
1) pip freeze > freeze.txt
2) pip install -r freeze.txt

 к выяснению и доработке
  СДЕЛАНО !!!!!  - если долго стоит работает - вылетает робот  - Process finished with exit code -1073740940 (0xC0000374)
    надо выяснить ошибку - так понимаю - ошибка с памятью связана - может многопоточность

  - что с летним/зимнем временем - pytz переключит ли?

  СДЕЛАНО !!!!!  - наблюдал - TWS хочет перезагружаться сам в 23-45, в это время работал робот - в 23-45 - коннект пропал
  робот вылетел с сообщением Disconnect после закрытия окна и Process finished with exit code -1073740791 (0xC0000409)
  2022-07-20 23:45:31,696 - robot - INFO - Нажали Disconnect
  2022-07-20 23:45:31,696 - robot - INFO - Зашли во внешний цикл робота


    - выводить время сервера - сейчас просто локальное время - проблема - можно каждый раз запрашивать -
  время сервера - но это через чур большое кол-во запросов; можно выводить через например каждый 10 раз;
  можно синхронизировать текуе часы робота и серверные - пробовал - но это гемор

    СДЕЛАНО !!!!!  - что если контракт не тот - уже старый

    СДЕЛАНО !!!!!  -  лицензия - файл mos.json - это по сути номер аккаунта - его надо будет читать наверное из файла какого-то - шифрованная запись


    СДЕЛАНО !!!!!  - если в позе в TWS и запускаем робота  - выбрасывает

    СДЕЛАНО !!!!!  -  если пихаю Log_r в функции типа orderStatus, openOrder - обработчики прерываний - выскакивают варнинги

    СДЕЛАНО !!!!!  - причина вылетов time_paper - иногда может  быть не корректен - неизвестного типа

    СДЕЛАНО !!!!!!!!!!!!!!! Стопы надо ставить GTC

    СДЕЛАНО !!!!!  - хранить не номера счетов, а их ХЕШи

    СДЕЛАНО !!!!!!!!!!!!!!!- если запустьить Коннект - потом открыть Сервис - потом закрыть Основное окно - то Сервис висит а
    а потом закрывается с ошибкой в терминале - т.е. при закрытии Основного окна, надо также чистить
    и закрвать Сервис

    СДЕЛАНО !!!!!!!!!!!!!!!- если запустить робота без TWS - робота выкидывает с ошибкой при нажатии на Коннект,
    надо чтобы робота не выкидывало, а писал, чтонет TWSа

    СДЕЛАНО !!!!!!!!!!!!!!!- если вдруг TWS ерезагружается - робот вылетает с ошибкой - надо чтобы робот висел - пытался соединять,
    но не вылетал

    СДЕЛАНО !!!!!!!!!!!!!!!- уведомления через емейл, телеграм - https://github.com/liiight/notifiers
    (см в телеграм канале Senior Python Developer)

    СДЕЛАНО !!!!  - включили робот - зашли в сделку - вышли из робота - включили робота - в указанное время закрыли сделоку.
                    НО стоп не убрался !!!!!!!!!!!!!!!!!! конфиг не почистился!!!!!!!!!!!!!!!!!!!!

    СДЕЛАНО !!!!!!!!!!!!!!!- если запустить робота + коннет без TWS - робот закрывается с ошибкой

    СДЕЛАНО !!!! - для телеграмма надо токен робота - узнаем при создании бота -  BotFather
        и нуже ID телеграмма человека - можно узнать у @userinfobot - при старте он пришлет ID человека
        https://ru.stackoverflow.com/questions/1335447/%D0%9A%D0%B0%D0%BA-%D1%81%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C-%D0%B1%D0%B5%D1%81%D0%BA%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D1%8B%D0%B9-%D1%86%D0%B8%D0%BA%D0%BB-%D0%B4%D0%BB%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D1%82%D0%B5%D0%BB%D0%B5%D0%B3%D1%80%D0%B0%D0%BC%D0%BC
        https://ru.stackoverflow.com/questions/1087059/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D1%82%D1%8C-long-polling-%D0%B8-schedule

    СДЕЛАНО !!!! -  ситуация - если инет есть + TWS запущен + робот апущен, далее пропадаает интернет - !!!! телеграм перестает работать,
        т.е. он  выходит из  polling - может слать через функцию send(), но отвечать он не может
        - надо как-то перезапускать телеграм после потери интернета

    СДЕЛАНО !!!! - надо поставить оповещение - если до смены бумаги осталось например 5 дней

    СДЕЛАНО !!!!!  - если делать Коннект - Дисконнект -> вылетает

    СДЕЛАНО !!!!!  - мы в позе - нажимаем сборос робота - поза закрывается - стоп остается!!!!!!!,
    если еще раз нажать Сброс - стоп убрался

    СДЕЛАНО !!!!!  - надо оповещение на телеграм при сделке - только на почту - нет оповещения о выходе из сделки

    На выходных, в воскресенье: TWS - не может сам загрузиться - надо вводить пароль - надо либо оповещение слать
    либо как-то вводить пароль (хотя если в этом случае вводишь - TWS ругается и надо закрыть его и опять открыть)
    !!! Вообщем это незибежно - на крайняк делать приблуду -> закрыла TWS - открыла TWS - ввела логин/пароль

    ПОПРОБОВАНО - Не очень((( -  торговля в Gate (не TWS)

    СДЕЛАНО !!!!!  -  выводить Ошибка соединения с сервером (когда пропадет коннект) - не в окно сообщений - засерается
    - а в одноразовое сообщение повыше - туда бы еще цвет добавить - чтобы моргало сообщение это
    - а еще опопвещение добавить на Ошибку соединения

    СДЕЛАНО !!!!!  - сделать прокрутку в Окне сообщение нормальное - чтобы само в низ моталось

    СДЕЛАНО !!!!!  -  добавить время в окно сообщений MessageInfo

    СДЕЛАНО !!!!!  - !!!!! был какой-то бак-зависание: была ошибка соединения с сервером - TWS сам разорвал - а робот почему-то
        не мог подсоединиться и как будто пытался создавать новые соединиея - новые соединения моргали в TWSе

    СДЕЛАНО !!!!!  - пропадание букв в MessageInfo -
         решение: https://ru.stackoverflow.com/questions/1130669/%D0%92%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B5-%D1%81-qtextbrowser-%D0%B8%D0%B7-%D0%B4%D1%80%D1%83%D0%B3%D0%BE%D0%B3%D0%BE-%D0%BF%D0%BE%D1%82%D0%BE%D0%BA%D0%B0

    СДЕЛАНО !!!!!  - сделать Риск настраиваемым

    СДЕЛАНО !!!!!  - проблема "9-06" - робот пытается соединиться - однако старое соединине еще действует
      и получается что на новое соединение опять пытается соединиться -
    т.е. в 9-06 робот думает что связь оборвалась, а на самом деле нет - но робот пытается соединистья

    СДЕЛАНО !!!!!  - надо разобраться с потоками - сигналы и слоты в QT5
    https://stackoverflow.com/questions/37252756/simplest-way-for-pyqt-threading/37256736#37256736

    СДЕЛАНО !!!!! -если робот запущен в выходные то у нас НЕТ цены в робота - Price = self.contract_price -
       т.е. во время нерабочего времени надо брать последнее закрытие где-то как-то


    СДЕЛАНО !!!!!  - когда связь с сервером пропдадает - робот начинает писать в окне и в телеге - Ошибка соединения.
    Соединиться не удалось - так вот может если мы уже в этом состоянии - то больше не выводить это сообщение
    и не слать в телегу

    ПОПРОБОВАНО - IB Gatey попробывать - работает не корректно, какие-то затупы
            - некоторые настройки в IBG, отсутству.т чем в TWS - вообщем это отдельная песьня

    СДЕЛАНО !!!!!- exe-шник сделать - https://pyinstaller.org/en/stable/index.html
        https://ru.stackoverflow.com/questions/1015456/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BA%D1%80%D1%8B%D1%82%D1%8C-%D0%BA%D0%BE%D0%BD%D1%81%D0%BE%D0%BB%D1%8C-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%B0-%D0%B8%D0%B7-python-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B
        команда pyinstaller --noconsole имя_вашего_скрипта.py
        pyinstaller --noconsole --windowed --icon=config/matreshka.ico SP500.py


     - другой комп, другую винду, (??? Linux)
        Запускается на  64-Win 11 pro, 64-Win 10 pro, 64-Win Server 2012 R2 Standart...


    СДЕЛАНО !!!!! V - сделать стандартные настроки

    СДЕЛАНО !!!!!-  когда Ошибка соединения - связь с сервером ставить в NO

    СДЕЛАНО !!!!!-  прогнать стратегию в ноябре на 09.11.2022 - норм

    СДЕЛАНО !!!!!- Live Trading ports: TWS: 7496; IB Gateway: 4001
    СДЕЛАНО !!!!!- Simulated Trading ports: TWS 7497; IB Gateway: 4002

    СДЕЛАНО !!!!!- Доделать в выходные - посмотреть ошибку - Инструкции для себя, для клиента

    СДЕЛАНО !!!!!- поменять иконку в приложении

    СДЕЛАНО !!!!!- разместить конфигурационные файлы (календарь, конфиг, мос, иконка) в отдельную папку

    СДЕЛАНО !!!!!- кнопу Сервис переименовать на Service

    СДЕЛАНО !!!!!- конец фьючерса в днях отсчитывать всегда - с самого начала

    СДЕЛАНО !!!!!-  матрешка крутится

    СДЕЛАНО !!!!!- реальный счет - нет CurrInitMargin - ошибка связана с запросом демо сделки Trade(... demo)
        - действительно система отвечает, что отсутствует разрешения на торговлю бумагой - галочики поставил - ждем
        - ошибка No trading permissions - галочки в ЛК поставил - надо ждать 48 часов - след неделя

    СДЕЛАНО !!!!!-  надо стопорить при увеличении процентов - минимальный депозит не может быть меньше Маржи !!!!!

    СДЕЛАНО !!!!!-  PreOrder вытащить в основное окно
    СДЕЛАНО !!!!!-  в инструкцию добавить PreDirection




"""
import json
import logging
import os
import sys
from threading import Thread
import time
from datetime import datetime, timedelta

import pytz
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame)

from PyQt5.QtCore import QCoreApplication, Qt, QThread, QMutex, pyqtSignal

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

# import logging
import queue
import socket
# import Interface
import sys

from ibapi import (decoder, reader, comm)
from ibapi.connection import Connection
from ibapi.message import OUT
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import Contract
from ibapi.order import Order, COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID
from ibapi.execution import ExecutionFilter
from ibapi.scanner import ScannerSubscription
from ibapi.comm import (make_field, make_field_handle_empty)
from ibapi.utils import (current_fn_name, BadMessage, intMaxString, decimalMaxString, floatMaxString, iswrapper)
from ibapi.errors import *  # @UnusedWildImport
from ibapi.server_versions import *  # @UnusedWildImport
from ibapi.utils import ClientException

# артефакт ля работы API
logger = logging.getLogger(__name__)

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
import time
import hashlib
import smtplib

# from notifiers import get_notifier

# if not os.path.exists("log"):
#     os.makedirs("log")
#
# log_r = logging.getLogger('robot')
# log_r.setLevel(logging.INFO)
# fh = logging.FileHandler()   #("log/robot.log", 'a', 'utf-8')  # каждый раз новый файл 'w', дозапись 'a'
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# log_r.addHandler(fh)

import SP500
import robot_telebot


def roundTick(cena, tick, param="+"):
    a = cena // tick  # количество тиков в цене
    b = cena % tick  # остаток от деления

    if b == 0:  # если остатка от деления нет
        с = tick * a
    elif param == '+':  # если нужно округлять в большую сторону
        с = (tick * a) + tick
    elif param == '-':  # если нужно округлять в меньшую сторону
        с = tick * a

    return с


def resvalacc(acc=""):
    md = hashlib.md5()
    my_str = acc  # "DU2079632_1"
    my_str = my_str[0::2] + my_str + my_str + my_str + my_str[0::3] + my_str[0::4]
    # my_str = my_str[0::2] + my_str + my_str + my_str + my_str[0::3] + my_str[0::4]
    print(my_str)
    md.update(my_str.encode('utf-8'))
    print(md.digest())
    print("Digest Size:", md.digest_size, "\n", "Block Size: ", md.block_size)

    # Comparing digest of SHA224, SHA256,SHA384,SHA512
    my_str_enc = hashlib.sha224(my_str.encode('utf-8')).hexdigest()
    print(my_str_enc)
    print("Digest SHA224", hashlib.sha224(my_str.encode('utf-8')).hexdigest())
    # print ("Digest SHA256", hashlib.sha256(my_str.encode('utf-8')).hexdigest())
    # print ("Digest SHA384", hashlib.sha384(my_str.encode('utf-8')).hexdigest())
    # print ("Digest SHA512", hashlib.sha512(my_str.encode('utf-8')).hexdigest())
    return my_str_enc


class RobotApp(QThread, EWrapper, EClient):
    # def __init__(self, mainwindow, servicewindow, email, telegram, telegram_interactive, *args, **kwargs):

    # создаем сигналы для QT!!!!
    # signal_textFoo = pyqtSignal(str)
    MessageInfoToQT = pyqtSignal(str)  # пишем в окно Message
    FromConfigToQT = pyqtSignal(dict)  # параметры, которые читаются из Конфига
    FromRobotAppToQT = pyqtSignal(dict)  # параметры обновляемые при работе алгоритма при коннекте
    # ButtonConnectToQT = pyqtSignal()  # посылаем нажатие кнопки Коннект
    FromRobotAppToQT_srv = pyqtSignal(dict)  # параметры обновляемые при работе алгоритма - посылаем в окно Сервис

    def __init__(self, mainwindow, servicewindow, email, *args, **kwargs):
        EClient.__init__(self, self)
        super(RobotApp, self).__init__(*args, **kwargs)

        # словарь сигналов в Основное окно

        self.signals_FromRobotAppToQT = {
            # "btn_connect": "a",
            "lbl_server_conn_Edit": "NO",
            "lbl_server_time_Edit": "-",
            "lbl_account_Edit": "-",
            "lbl_account_size_Edit": "-",
            "lbl_available_funds_Edit": "-",
            "lbl_working_time_Edit": "-",
            "lbl_paper_price_Edit": "-",
            "lbl_min_depo_Edit": "-",
            "lbl_order_direction_Edit": "-",
            "lbl_robot_state_Edit": "-",
            "lbl_direction_Edit": "-",
            "lbl_position_size_Edit": "0",
            "lbl_price_input_trade_Edit": "0",
            "lbl_price_stop_trade_Edit": "0",
            "empty": "0"
        }
        # словарь сигналов в окно Сервис
        self.signals_FromRobotAppToQT_srv = {
            "lbl_work_session_Edit": "-",
            "lbl_direction_Edit": "-",
            "lbl_week_day_Edit": "-",
            "lbl_days_in_trend_Edit": "-",
            "lbl_trend_delta_Edit": "-",
            "lbl_order_direction_Edit": "-",
            "lbl_available_funds_Edit": "-",
            "lbl_go_Edit": "-",
            "lbl_svv_Edit": "-",
            "lbl_relative_stop_Edit": "-",
            "lbl_absolute_stop_Edit": "-",
            "lbl_loss_1_lot_Edit": "-",
            "lbl_abs_loss_1_trade_Edit": "-",
            "lbl_number_of_lot_Edit": "-",
            # "flag_change_config": "-",
            # "flag_reset": "-",
        }

        self.contract_price_last = 0
        self.flag_reset = False
        self.lastTradeDate = ""
        self.contract_details = None
        self.telegram_id = ""
        self.telegram_token = ""
        self.to_addr_email = ""
        self.order_direction = "None"
        self.flag_5_min_candle = False
        self.price_stop_trade = 0
        self.price_input_trade = 0
        self.price_input_trade_avg = 0
        self.flag_read_5mins = False
        self.currency_account = ""
        self.pip_price = 0
        self.go = 0
        self.AvailableFunds = ""
        self.free_money = 0
        self.risk = 0
        self.minTick = 0
        self.svv_day = 0
        self.stop_percent = 0
        self.delta_trend = 0
        self.flag_day_candle = False
        self.index_day_candle = 1
        self.day_candle = {}
        # self.day_candle_tmp = {}
        self.flag_openOrderEnd = False
        self.simplePlaceOid = None
        self.flag_error_message = False
        self.nextValidOrderId = 1
        self.flag_error_201 = False
        self.flag_error_460 = False
        self.message_error = ""
        self.param_execDetails = {}
        self.param_openOrder = {}
        self.param_orderStatus = {}
        self.flag_openOrder = False
        self.old_str_openOrder = ""
        self.str_openOrder = ""
        self.old_str_orderStatus = ""
        self.str_orderStatus = ""
        self.flag_orderStatus = False
        self.execution_shares = 0
        self.flag_execDetails = False
        self.flag_contract_price_change = False
        self.NetLiquidation = "-"
        self.flag_NetLiquidation_change = False
        self.flag_position_change = False
        self.position = 0
        self.flag_account_with_server = False
        self.account = None
        self.mos = {}  # словарь
        self.mos_list = []  # список значений
        self.market_Data_Type = None
        self.contract_price = None
        self.flag_tickPrice = False
        self.flag_contractDetails = False

        self.time_to_act = {}
        self.server_tz = None
        self.server_weekday = None
        self.server_time_all = None
        self.flag_read_config = False
        self.flag_read_calendar = False
        self.flag_read_mos = False
        self.client_id = None
        self.port = None
        self.host = None
        # self.nextOrderId = 1
        self.mainwindow = mainwindow  # получаем доступ к основному окну
        self.servicewindow = servicewindow  # получаем доступ к сервисному окну
        self.email = email  # получаем доступ к емейлу
        # self.telegram = telegram
        # self.telegram_interactive = telegram_interactive
        self._mutex = QMutex()
        self.server_time = None
        self.contract_1 = {}
        self.contract_tz = "non"
        self.flag_Position = False  # мы в позе True, мы не в позе False
        self.tdw = {}
        self.tdm = {}
        self.NUM_DAY_CANDLE = 25  # количество считываемых свечек
        # QThread.daemon = True  # выключает поток при закрытии интерфейса

    # def connectionClosed(self):
    #     print('46')
    #     EClient.disconnect()
    # посылки в Основное окно
    def set_FromRobotAppToQT(self, param="", text=""):
        self.signals_FromRobotAppToQT[param] = text
        self.FromRobotAppToQT.emit(self.signals_FromRobotAppToQT)  # [param])

    # посылки в окно Сервис
    def set_FromRobotAppToQT_srv(self, param="", text=""):
        self.signals_FromRobotAppToQT_srv[param] = text
        self.FromRobotAppToQT_srv.emit(self.signals_FromRobotAppToQT_srv)

    # сюда приходит текущее время с сервера
    def currentTime(self, time: int):
        """ Server's current time. This method will receive IB server's system
                time resulting after the invokation of reqCurrentTime. """
        self.server_time_all = time
        self.server_time = datetime.fromtimestamp(time).strftime("%A, %B %d, %Y %H:%M:%S")

        # # time1 = datetime.fromtimestamp(time).strptime("%A, %B %d, %Y %H:%M:%S")
        # # time2 = datetime.fromtimestamp(datetime.utcnow()).strptime("%A, %B %d, %Y %H:%M:%S")
        # # print('time1',time1)
        # # print('time2',time2)
        # print('currentTime: ', datetime.fromtimestamp(time).strftime("%A, %B %d, %Y %H:%M:%S")) # - datetime.utcnow())
        # print('currentTime: ', datetime.utcnow().strftime("%A, %B %d, %Y %H:%M:%S"))  # - datetime.utcnow())
        # t1 = datetime.fromtimestamp(time)#.strftime("%A, %B %d, %Y %H:%M:%S")
        # t2 = datetime.utcnow()#.strftime("%A, %B %d, %Y %H:%M:%S")
        # # print('currentTime:', datetime.now() - datetime.utcnow())
        # t3 = t1 - t2
        # dh = t1.hour - t2.hour
        # print('currentTime:', dh)

        self.server_tz = datetime.fromtimestamp(time).timetz()
        self.server_weekday = datetime.fromtimestamp(time).weekday()
        print('server_weekday:', self.server_weekday)

    @iswrapper
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        # self.message_error = f'Error: reqId: {reqId}, errorCode: {errorCode}, message: {errorString}'
        self.message_error = "Error: " + str(reqId) + " " + str(errorCode) + " " + errorString

        # print("Error: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson)
        # logging.critical("Error: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson)
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        if advancedOrderRejectJson:
            print("error: Id:", reqId, "Code:", errorCode, "Msg:", errorString, "AdvancedOrderRejectJson:",
                  advancedOrderRejectJson)
            logging.critical("error: Id:", reqId, "Code:", errorCode, "Msg:", errorString, "AdvancedOrderRejectJson:",
                             advancedOrderRejectJson)
        else:
            print("error: Id:", reqId, "Code:", errorCode, "Msg:", errorString)
            logging.critical("error: Id:", reqId, "Code:", errorCode, "Msg:", errorString)

        # if reqId != -1:
        self.flag_error_message = True
        # ловим ошибку 201 - послали контрактов больше чем может проглотить
        if errorCode == 201:
            self.flag_error_201 = True
        # ошибка No trading permissions - отсутствует разрешение на торговлю инструментом
        # решается:  You just need to go to your
        # Account Management > Trading Permissions to enable the required settings
        if errorCode == 460:
            self.flag_error_460 = True

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        # self.nextOrderId = orderId
        self.nextValidOrderId = orderId
        # log_r.info('nextValidId: ', orderId)
        print('nextValidId: ', orderId)

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange,
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:",
              averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        # ловим размер позиции
        if contract.symbol == self.contract_1['symbol']:
            self.position = int(position)
            self.flag_position_change = True

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)
        # ловим размер счета
        if key == 'NetLiquidation':  # активов всего = лоты + деньги
            self.flag_NetLiquidation_change = True
            self.NetLiquidation = f'{val} {currency}'
            self.currency_account = currency
        if key == 'AvailableFunds':  # кол-во свободных денег или как вариант 'FullAvailableFunds'
            self.AvailableFunds = f'{val} {currency}'
            self.free_money = float(val)
            self.flag_NetLiquidation_change = True

    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName: str):
        print("AccountDownloadEnd. Account:", accountName)
        self.account = accountName
        self.flag_account_with_server = True

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        self.str_orderStatus = f'OrderStatus. Id: {orderId}, {status}, {filled}, {remaining}, {avgFillPrice}, {permId},\
                               {parentId}, {lastFillPrice}, {clientId}, {whyHeld}, {mktCapPrice}'
        # если новая строка не равна старой строке - печатаем - защита от дублирования сообщений
        if self.old_str_orderStatus != self.str_orderStatus:
            print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining,
                  ", LastFillPrice: ", lastFillPrice, ", avgFillPrice: ", avgFillPrice)
            self.param_orderStatus = {'orderId': orderId, 'status': status, 'filled': filled, 'remaining': remaining,
                                      'lastFillPrice': lastFillPrice, 'avgFillPrice': avgFillPrice}
            # log_r.info("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ",
            # remaining, ", LastFillPrice: ", lastFillPrice)
            self.flag_orderStatus = True

        self.old_str_orderStatus = self.str_orderStatus

    def openOrder(self, orderId, contract, order, orderState):
        self.str_openOrder = f'OpenOrder. Id: {orderId}, {contract}, {order}, {orderState}'
        if self.old_str_openOrder != self.str_openOrder:
            print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":",
                  order.action, order.orderType, order.totalQuantity, orderState.status)
            print(orderState.status, orderState.initMarginBefore, orderState.maintMarginBefore,
                  orderState.equityWithLoanBefore, "1:", orderState.initMarginChange, orderState.maintMarginChange,
                  orderState.equityWithLoanChange, orderState.initMarginAfter, orderState.maintMarginAfter,
                  orderState.equityWithLoanAfter, orderState.commission, orderState.minCommission,
                  orderState.maxCommission, orderState.commissionCurrency, orderState.warningText,
                  orderState.completedTime, orderState.completedStatus)
            if (float(orderState.initMarginChange) > 0) \
                    and (float(orderState.initMarginChange) < 1000000):  # защита - проскакивают очень большие числа
                # - если большое число - просто не учитываем
                self.go = float(orderState.initMarginChange)
            print('go =', self.go)

            if contract.localSymbol == self.contract_1['localSymbol']:
                self.param_openOrder = {'orderId': orderId, 'contract': contract, 'order': order,
                                        'orderState': orderState}
                self.flag_openOrder = True
            # log_r.info("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":",
            #            order.action, order.orderType, order.totalQuantity, orderState.status)

            # print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId),
            #       " OrderId:", intMaxString(orderId), "Account:", order.account, "Symbol:", contract.symbol, "SecType:",
            #       contract.secType,
            #       "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
            #       "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty),
            #       "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:",
            #       orderState.status,
            #       "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:",
            #       intMaxString(order.minCompeteSize),
            #       "competeAgainstBestOffset:",
            #       "UpToMid" if order.competeAgainstBestOffset == COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID else floatMaxString(
            #           order.competeAgainstBestOffset),
            #       "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole), "MidOffsetAtHalf:",
            #       floatMaxString(order.midOffsetAtHalf))
            # self.flag_openOrder = True

        self.old_str_openOrder = self.str_openOrder

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)
        self.flag_execDetails = True  # сделка совершена на кол-во лотов  = execution.shares
        self.param_execDetails = {'contract': contract, 'execution': execution}
        # log_r.info("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
        #            execution.orderId, execution.shares, execution.lastLiquidity)

    # если отправляли запрос на чтение позиций, ордеров
    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")
        self.flag_openOrderEnd = True

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')
        # word = 0
        # if self.market_Data_Type == 3:  # если мы получаем данные с задержкой
        #     word = 68  # 'DELAYED_LAST' или 68
        # elif self.market_Data_Type == 1:  # если мы получаем данные живые
        #     word = 4  # 'LAST_PRICE'-проверить?  или 4
        #
        # if tickType == word:
        #     # if TickTypeEnum.to_str(tickType) == word:   # из ряда цен будем выбирать под типом LAST
        #     self.contract_price = price
        #     self.flag_tickPrice = True
        # else:
        #     self.flag_tickPrice = False

        if (tickType == 68) or (tickType == 4):
            self.flag_contract_price_change = True
            self.contract_price = price
            # self.flag_tickPrice = True

    # def tickSize(self, reqId, tickType, size):
    #     print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        print("MarketDataType. ReqId:", reqId, "Type:", marketDataType)
        self.market_Data_Type = marketDataType

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)
        # получаем временную зону контракта
        self.pip_price = int(contractDetails.contract.multiplier)
        self.minTick = contractDetails.minTick
        self.contract_tz = contractDetails.timeZoneId
        self.contract_details = contractDetails
        self.flag_contractDetails = True

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low,
              "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.wap)
        # заполняем массив свечек
        # if self.flag_read_5mins:
        #     self.price_input_trade = float(bar.open)
        # else:
        self.day_candle[self.index_day_candle]['dt'] = bar.date
        self.day_candle[self.index_day_candle]['o'] = bar.open
        self.day_candle[self.index_day_candle]['h'] = bar.high
        self.day_candle[self.index_day_candle]['l'] = bar.low
        self.day_candle[self.index_day_candle]['c'] = bar.close
        self.index_day_candle += 1

    def historicalDataEnd(self, reqId, start, end):
        print("historicalDataEnd. ", reqId, " start:", start, "end:", end)

        if self.flag_read_5mins:
            self.flag_read_5mins = False
            self.flag_5_min_candle = True
        else:
            self.index_day_candle -= 1
            if self.index_day_candle == self.NUM_DAY_CANDLE:
                # self.day_candle = self.day_candle_tmp
                print("historicalDataEnd. Массив свечек заполнен", self.index_day_candle, "=", self.NUM_DAY_CANDLE)
                self.flag_day_candle = True
                # self.contract_price_close = self.day_candle[self.index_day_candle]["c"]
                # print(f"Сегодняшнее закрытие - {self.contract_price_close}")
            else:
                print("historicalDataEnd. Массив свечек не корректен", self.index_day_candle, "!=",
                      self.NUM_DAY_CANDLE)
                self.flag_day_candle = False

    def message_handler_terminal(self):
        try:
            try:
                print("log0")
                text = self.msg_queue.get(block=True, timeout=0.2)
                if len(text) > MAX_MSG_LEN:
                    self.wrapper.error(NO_VALID_ID, BAD_LENGTH.code(),
                                       "%s:%d:%s" % (BAD_LENGTH.msg(), len(text), text))
                    logging.critical(f'Ошибка длины сообщения: len={len(text)}, {text}')
                    print(f'Ошибка длины сообщения: len={len(text)}, {text}')
                    return  # break
            except queue.Empty:
                print("log1")
                # logging.critical(f'log1: Ошибка пустоты: queue.get: empty')
                logger.debug("queue.get: empty")
                self.msgLoopTmo()
            else:
                print("log2")
                fields = comm.read_fields(text)
                logger.debug("fields %s", fields)
                self.decoder.interpret(fields)
                self.msgLoopRec()
        except (KeyboardInterrupt, SystemExit):
            print("log3")
            logger.info("detected KeyboardInterrupt, SystemExit")
            self.keyboardInterrupt()
            self.keyboardInterruptHard()
        except BadMessage:
            print("log4")
            logger.info("BadMessage")

        logger.debug("conn:%d queue.sz:%d",
                     self.isConnected(),
                     self.msg_queue.qsize())

    # переопределяем disconnect = как в client.py, т.к. у QT тоже есть такая функция
    # поэтому если обращаться по умолчанию - идет конфликт
    def disconnect(self):
        """Call this function to terminate the connections with TWS.
        Calling this function does not cancel orders that have already been
        sent."""
        self.setConnState(EClient.DISCONNECTED)
        if self.conn is not None:
            logger.info("disconnecting")
            self.conn.disconnect()
            self.wrapper.connectionClosed()
            self.reset()

    def MessageInfo(self, text):
        txt = datetime.now().strftime("%d.%m.%Y, %H:%M:%S - ") + text
        # self.mainwindow.lbl_Message_Edit.append(txt)
        self.MessageInfoToQT.emit(txt)

    # посылаем почтовое сообщение
    def MessageEmail(self, subject, to_addr, text):
        self.email.host_email = "smtp-mail.outlook.com: 587"
        self.email.subject_email = subject  # "Subscription" + str(self.i)
        self.email.to_addr_email = to_addr  # "mikhaillapov12@gmail.com"
        self.email.from_addr_email = "robot_sp@hotmail.com"
        self.email.password_email = "Abyrvalg44!"
        self.email.body_text_email = text  # "begin" + str(self.i)

        if to_addr.find("@") != -1:  # если собачка есть в адресе как-то - то конструкция должна вернуть True
            self.email.flag_sent_email = True
        else:
            print("Адрес почты не содержит знак - @. Email не отправлен!")

    # читаем каледарь
    def ReadMOS(self):
        self.flag_read_mos = True
        try:
            with open("config/mos.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл config/mos.json отсутствует')
            logging.critical('Файл config/mos.json отсутствует')  # log_r.critical('Файл mos.json отсутствует')
            self.MessageInfo('Файл config/mos.json отсутствует')
            # !!!!! вывод ошибки в окно сообщений робота
            return False

        print(f'mos: {loaded_json_file}')
        logging.info(f'mos: {loaded_json_file}')  # log_r.info(f'mos: {loaded_json_file}')

        self.mos = loaded_json_file["mos"]
        self.mos_list = list(self.mos.values())
        # self.risk = loaded_json_file["risk"]

        return True

    # читаем каледарь
    def ReadCalendar(self):
        self.flag_read_calendar = True
        try:
            with open("config/calendar.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл config/calendar.json отсутствует')
            logging.critical('Файл config/calendar.json отсутствует')
            self.MessageInfo('Файл config/calendar.json отсутствует')
            # !!!!! вывод ошибки в окно сообщений робота
            return False

        print(f'calendar: {loaded_json_file}')
        logging.info(f'calendar: {loaded_json_file}')

        self.tdw = loaded_json_file["Week"]
        self.tdm = loaded_json_file["Month"]
        return True

    # читаем конфиг
    def ReadConfig(self):

        self.flag_read_config = True
        try:
            with open("config/config.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл config/config.json отсутствует')
            logging.critical('Файл config/config.json отсутствует')
            self.MessageInfo('Файл config/config.json отсутствует')
            return False

        print(f'config: {loaded_json_file}')
        logging.info(f'config: {loaded_json_file}')
        self.host = loaded_json_file["Host"]  # print(f'хост: {loaded_json_file["Host"]}') # по умолчанию 127.0.0.1
        # port - TWS demo 7497, IB Gateway demo 4002, TWS real 7496, IB Gateway real 4001
        self.port = int(
            loaded_json_file["Port"])  # print(f'port: {loaded_json_file["Port"]}') # по умолчанию 7497 - demo
        self.client_id = int(
            loaded_json_file["Client ID"])  # print(f'id: {loaded_json_file["Client ID"]}') # по умолчанию 1
        self.contract_1 = loaded_json_file["Contract"]  # print(f'id: {loaded_json_file["Contract"]}')  # по умолчанию 1
        self.time_to_act = loaded_json_file["Time_to_act"]
        self.delta_trend = loaded_json_file["delta"]
        self.svv_day = loaded_json_file["svv"]
        self.stop_percent = loaded_json_file["stop_percent"]
        self.price_input_trade_avg = loaded_json_file["price_input_avg"]
        self.price_input_trade = loaded_json_file["price_input"]
        self.price_stop_trade = loaded_json_file["price_stop"]
        self.to_addr_email = loaded_json_file["Email"]
        self.telegram_token = loaded_json_file["Telegram_token"]
        self.telegram_id = loaded_json_file["Telegram_id"]
        self.lastTradeDate = loaded_json_file["lastTradeDate"]
        self.risk = int(loaded_json_file["risk"])
        self.contract_price = loaded_json_file["price_last"]

        # self.order_direction = loaded_json_file["direction"]

        # self.mainwindow.lbl_host_Edit.setText(str(self.host))
        # self.mainwindow.lbl_port_Edit.setText(str(self.port))
        # self.mainwindow.lbl_client_id_Edit.setText(str(self.client_id))
        # self.mainwindow.lbl_paper_Edit.setText(str(self.contract_1["localSymbol"]))
        # self.mainwindow.lbl_risk_Edit.setText(str(self.risk) + "%")
        self.FromConfigToQT.emit({"lbl_host_Edit": str(self.host),
                                  "lbl_port_Edit": str(self.port),
                                  "lbl_client_id_Edit": str(self.client_id),
                                  "lbl_paper_Edit": str(self.contract_1["localSymbol"]),
                                  "lbl_risk_Edit": str(str(self.risk) + "%")
                                  })
        return True

    def R_W_config(self, param="", val=None):
        # читаем файл конфига
        with open("config/config.json", "r") as read_file:
            loaded_json_file = json.load(read_file)
        # перезаписываем данные
        loaded_json_file[param] = val
        # записываем в конфиг обратно
        # Запись в файл:
        with open("config/config.json", "w") as write_file:
            json.dump(loaded_json_file, write_file, indent=4)

    def Trade(self, contract=Contract(), trd="", order_direction="", position=0, contract_price=0, orderType="LMT",
              real="real"):
        # order_direction = ""
        price_input = 0

        number_of_lot = abs(position)

        if trd == "INPUT":
            if order_direction == "BUY":
                # если покупаем, берем цену на 10% выше текущей цены
                price_input = ((contract_price * 11) // 10)
            elif order_direction == "SELL":
                # если продаем, берем цену на 10% ниже текущей цены
                price_input = ((contract_price * 9) // 10)
            else:
                print('Trade: Направление для сделки (BUY,SELL) не задано')
                logging.info(f'Trade: Направление для сделки (BUY,SELL) не задано')
                self.MessageInfo(f'Trade: Направление для сделки (BUY,SELL) не задано')
                return
        elif trd == "OUTPUT":
            if position > 0:  # мы в лонгах
                order_direction = "SELL"  # продаем по цене ниже рынка
                price_input = ((contract_price * 9) // 10)
            elif position < 0:  # мы в шортах
                order_direction = "BUY"  # покупаем по цене выше рынка
                price_input = ((contract_price * 11) // 10)
            else:
                print('Trade: Хотим совершить сделку на 0 контрактов!')
                logging.info(f'Trade: Хотим совершить сделку на 0 контрактов!')
                self.MessageInfo(f'Trade: Хотим совершить сделку на 0 контрактов!')
                return
        else:
            print('Trade: Направление для сделки (INPUT,OUTPUT) не определено')
            logging.info(f'Trade: Направление для сделки (INPUT,OUTPUT) не определено')
            self.MessageInfo(f'Trade: Направление для сделки (INPUT,OUTPUT) не определено')
            return

        order = Order()
        # формируем ордер
        order.action = order_direction
        order.totalQuantity = number_of_lot
        order.orderType = orderType
        order.lmtPrice = price_input
        order.whatIf = False if real == "real" else True  # если не реальная сделка то True

        self.placeOrder(self.nextOrderId(), contract, order)

    def run(self):
        # self._mutex.lock()
        time_paper = datetime
        flag_flag_connect_old = False
        flag_correct_config = False
        flag_correct_calendar = False
        flag_correct_mos = False
        flag_time_paper = False
        contract_subtractor = 0
        absolute_stop = 0
        flag_input = False
        flag_output = False
        flag_need_output = False
        flag_create_telegram = False
        cnt_reqHistoricalData = 0  # счетчик для чтения свечек
        flag_time_first_min = False
        # time_for_reset = datetime
        cnt_reset = 0
        cnt_stop = 0
        tmp_min = 0
        exit_reason = "None"  # указывается причина выхода из сделки
        day_old = 0
        trig_reqHistory = 1000  # надо быть числом отличным от 0-59
        flag_isCon = False
        flag_error_460_1 = False

        cnt_request = 0  # счетчик медленных запросов
        CNT_REQ = 100  # запрашиваем 1 через 10 раз
        num_month = ""
        work_session = 0
        week_day = 0
        # DELTA_TREND = 2  # порог дельта в тренде
        day_old = 0
        cnt_error_connect = 0
        flag_error_connect = False
        avgfillprice = 0
        # конфигурируем почту

        # self.MessageEmail(subject="Тест 1", to_addr="mikhaillapov12@gmail.com", text="Тест 1")

        dict_week_day = {0: "Monday ", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday",
                         6: "Sunsday"}
        # order_direction = "None"
        # self.day_candle_tmp = {a: {'dt': "", 'o': 0, 'h': 0, 'l': 0, 'c': 0} for a in range(1, self.NUM_DAY_CANDLE+1)}
        self.day_candle = {a: {'dt': "", 'o': 0.0, 'h': 0.0, 'l': 0.0, 'c': 0.0} for a in
                           range(1, self.NUM_DAY_CANDLE + 1)}
        a = 0
        loss_1_lot = 0
        req = 1
        # try:
        print('123')

        # определяем объекты
        order = Order()
        contract = Contract()

        # log_r.info('-------------- Новая Сессия ---------------')
        # self.MessageInfo('-------------- Новая Сессия ---------------')
        # email = get_notifier("email")
        # email.notify(username="mikhaillapov12@gmail.com", password="Girlyanda44", to="mikhaillapov@gmail.com",
        #              message="абырвалг2")
        # основной цикл робота
        # Читаем конфиг
        # Если конфига нет - выдаем ошибку и ничего не делаем

        while True:
            # logging.debug('debug')
            # logging.info('info')
            # logging.warning('warning')
            # logging.error('error')
            # logging.critical('critical')

            # проверка на нажатие кнопки Connect
            # если Была нажата Connect - соединяемся c сервером

            if self.mainwindow.flag_connect:

                # проверка на корректность конфига
                if (not flag_correct_config) or (not flag_correct_calendar) or \
                        (not flag_correct_mos):  # если конфиг, календарь или MOS не корректен - выходим

                    # self.mainwindow.flag_connect = False
                    flag_flag_connect_old = False
                    # self.mainwindow.btn_connect.setText('Connect')
                    self.mainwindow.button_Connect()  # делаем дисконнект
                    # self.ButtonConnectToQT.emit() #"button_Connect")
                    continue

                logging.critical('Зашли во внешний цикл робота')
                flag_flag_connect_old = True
                print("v1")

                # пытаемся соединиться с сервером
                try:
                    self.connect(self.host, self.port, self.client_id)
                    print("v2")
                    # конфигурируем наш контракт
                    contract.symbol = self.contract_1['symbol']
                    contract.secType = self.contract_1['secType']
                    contract.exchange = self.contract_1['exchange']
                    contract.currency = self.contract_1['currency']
                    contract.localSymbol = self.contract_1['localSymbol']
                    print("v3")
                    time.sleep(0.5)
                    self.reqContractDetails(self.nextOrderId(), contract)

                    time.sleep(0.1)
                    self.reqMarketDataType(1)  # (3)  # switch to delayed-frozen data if live is not available
                    # 1 - реальные данные, 3 - с задержкой
                    time.sleep(0.1)
                    self.reqMktData(self.nextOrderId(), contract, "", False, False, [])

                    time.sleep(0.1)
                    # self.reqIds()
                    # time.sleep(1)
                    # запрос данных о нашем контракте

                    # self.reqIds()
                    # запрос времени с сервера (единичный, потокового нет)
                    self.reqCurrentTime()  # -> def currentTime() -> server_time
                    time.sleep(0.1)
                    print("reqAccountUpdates")
                    self.reqAccountUpdates(True, "")
                    time.sleep(0.1)
                    # self.reqHistoricalData(self.nextOrderId(), contract, "", "10 D", "1 day", "TRADES", 0, 1, False, [])
                    # time.sleep(0.1)
                    # self.telegram.flag_sent_telegram = True
                    # self.telegram_interactive.flag_sent_telegram = True
                    # tB1.flag_sent_telegram = True
                    # tB2.flag_sent_telegram = True
                    print("v4")
                    # try:
                    #     tB2.send(f"Connect - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")  # .send_message(987861324, f"Коннект!!!! ") #self.telegram_id
                    # except Exception as e:
                    #     print(f"Ошибка v4{e}")
                    # try:
                    #     logging.error(f"Connect - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")
                    # except Exception as e:
                    #     print(f"Ошибка v4{e}")
                    # сверяем полученный аккаунт c сервера и разрешенными аккаунтами в файле
                    print("зашли в коннект")

                    # self.reqAllOpenOrders()
                    a = 0
                    flag_account_true = False
                    self.flag_position_change = True  # прочитаем позицию при входе в основной цикл
                    flag_one_trade = False  # флаг одной попытки для сделки
                    cnt_reqHistoricalData = 0
                    cnt_error_connect = 0
                    # flag_error_connect = False
                    flag_isCon = False
                    flag_error_460_1 = False
                    flag_number_of_lot_0 = False
                except:
                    print("Ошибка соединения. Соединиться с сервером не удалось.")
                    if not flag_error_connect:
                        tB2.send(
                            f"Connection error. Failed to connect to server. - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")
                        logging.error('Ошибка соединения. Соединиться с сервером не удалось.')
                        self.MessageInfo('Ошибка соединения. Соединиться с сервером не удалось.')
                        flag_error_connect = True

                    # заплатка - на случай если подсоединиться к серверу не можем - а нажали закрыть приложение
                    if self.mainwindow.close_app:
                        # self.mainwindow.flag_connect = False
                        self.mainwindow.button_Connect()  # делаем дисконнект
                        # self.ButtonConnectToQT.emit()  #"button_Connect")

                    # Заплатка на 5 ошибок "Ошибка соединения"
                    cnt_error_connect += 1
                    if cnt_error_connect == 5:
                        self.mainwindow.button_Connect()  # делаем дисконнект
                        # self.ButtonConnectToQT.emit()  #"button_Connect")
                        self.flag_reset = True  # а затем этот флаг нам опять просто включит Коннект

                    time.sleep(2)
                finally:
                    self.set_FromRobotAppToQT(param="empty", text="0")

                try:
                    while self.isConnected() or not self.msg_queue.empty():
                        print("f0.7")

                        if not flag_isCon:
                            flag_isCon = True
                            flag_error_connect = False
                            try:
                                tB2.send(f"Connect - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")
                            except Exception as e:
                                print(f"Ошибка f0.7: {e}")
                            try:
                                logging.error(f"Connect - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")
                            except Exception as e:
                                print(f"Ошибка f0.7: {e}")
                            self.set_FromRobotAppToQT(param="lbl_paper_price_Edit",
                                                      text=f"{format(self.contract_price, '.2f')}")

                        # log_r.info('Зашли во внутренний цикл - цикл isConnect')
                        # self.mainwindow.lbl_server_conn_Edit.setText('YES')
                        # self.signals_FromRobotAppToQT["lbl_server_conn_Edit"] = "YES"
                        # self.FromRobotAppToQT.emit(self.signals_FromRobotAppToQT["lbl_server_conn_Edit"])
                        self.set_FromRobotAppToQT(param="lbl_server_conn_Edit", text="YES")
                        print("f0.8")
                        # слушаем ответы от терминала
                        self.message_handler_terminal()
                        print("f0.9")
                        a = a + 1
                        print('aс = ', a)
                        print("f1")
                        if flag_account_true:  # если аккаунт валидный
                            # Основная программа тут
                            # Ждем время захода, если мы не в позиции
                            # try:
                            if flag_time_paper:  # if time_paper:  #контракт читали и время бумаги уже не None

                                # мы не в позе
                                if not self.flag_Position:
                                    try:
                                        # !!!!! для дебага. начало
                                        # self.order_direction = "BUY"
                                        # number_of_lot = 20
                                        # absolute_stop = 3625
                                        # !!!!! для дебага. ко5нец
                                        if time_paper.hour == int(self.time_to_act['input_hour']) \
                                                and time_paper.minute == int(self.time_to_act['input_min']) \
                                                and int(self.time_to_act['input_sec']) <= time_paper.second \
                                                and self.order_direction != "None" \
                                                and (week_day != 4 and week_day != 5) \
                                                and not flag_one_trade \
                                                and number_of_lot > 0 \
                                                and cnt_reset == 0 and cnt_stop == 0:  # сюда пока не заходили

                                            print("Время заходить")
                                            logging.critical("Время заходить")
                                            self.MessageInfo(f'Время заходить')
                                            flag_one_trade = True
                                            # time_for_reset = time_paper.time()
                                            # flag_time_first_min = True
                                            cnt_reset = 0
                                            cnt_stop = 0
                                            # print(f'Время для резета1: {time_for_reset}')
                                            # print(f'Время для резета2: {time_paper.time()}')
                                            # читаем текущую котировку
                                            # Считаем - сегодня вообще заходим

                                            # !!!!! для Debug. Начало
                                            # order_direction = "BUY"  # закомментировать для обычной работы
                                            # !!!!! для Debug. Конец

                                            number_of_lot -= contract_subtractor  # кол-во лотов, рассчитывается от риска - НАДО!!!
                                            if number_of_lot <= 0:
                                                number_of_lot = 0
                                            logging.info(
                                                f'Направление {self.order_direction}, кол-во контрактов {number_of_lot}')
                                            self.MessageInfo(
                                                f'Направление {self.order_direction}, кол-во контрактов {number_of_lot}')

                                            # рассчитываем стоп
                                            # absolute_stop = 4000

                                            self.Trade(contract=contract, trd="INPUT",
                                                       order_direction=self.order_direction,
                                                       position=number_of_lot, contract_price=self.contract_price,
                                                       orderType="LMT")
                                            # запишем в конфиг ориентировочную цену входа
                                            # цена входа = откртие свечи на которой зашли
                                            # для этого будем читать текущую 5-ти минутку
                                            #
                                            # self.reqHistoricalData(self.nextOrderId(), contract, "",
                                            #                        "1 D", "5 mins", "TRADES", 0, 1, False, [])
                                            # print("Заказываем 5 мин")
                                            # self.flag_read_5mins = True
                                            flag_input = True
                                            # time.sleep(0.1)
                                    except Exception as e:
                                        print(f"Ошибка в time_paper")
                                        print(f"Ошибка: {time_paper}: {e}")


                                # мы в позе
                                else:
                                    print('1:', flag_one_trade)
                                    # ждем время выхода
                                    if time_paper.hour == int(self.time_to_act['output_hour']) \
                                            and time_paper.minute == int(self.time_to_act['output_min']) \
                                            and int(self.time_to_act['output_sec']) <= time_paper.second \
                                            and (week_day != 5 and week_day != 6) \
                                            and not flag_one_trade:  # не выходим в Сб и Вс

                                        print("Время выходить")
                                        logging.critical("Время выходить")
                                        self.MessageInfo(f'Время выходить')
                                        flag_one_trade = True

                                        # Принятие решения - выходим или оставляем на следующий день
                                        # if self.price_input_trade = 0
                                        # flag_need_output = True  # !!!!! надо сбрасывать после обнуления позиции

                                        # если мы в лонгах
                                        if self.position > 0:
                                            # и если мы выше точки входа - выходим
                                            if self.contract_price >= self.price_input_trade:
                                                flag_need_output = True
                                        # если мы в шортах
                                        elif self.position < 0:
                                            # и если мы ниже точки входа - выходим
                                            if self.contract_price <= self.price_input_trade:
                                                flag_need_output = True
                                        else:
                                            flag_need_output = False
                                        print(f"Позиция: {self.position} \n"
                                              f"Текущая цена: {self.contract_price} \n"
                                              f"Цена теор. входа: {self.price_input_trade}")

                                        # если нужно выходить
                                        if flag_need_output:
                                            self.Trade(contract=contract, trd="OUTPUT", position=self.position,
                                                       contract_price=self.contract_price, orderType="LMT")
                                            flag_output = True
                                            exit_reason = "Profit"
                                            print("Выходим")
                                        else:
                                            print("Переносим позицию на следующий день")
                                            logging.critical("Переносим позицию на следующий день")
                                            self.MessageInfo(f'Переносим позицию на следующий день')

                                # костыль против повторного сброса во время минуты захода
                                if time_paper.hour == int(self.time_to_act['input_hour']) and \
                                        time_paper.minute == int(self.time_to_act['input_min']):
                                    flag_time_first_min = True
                                    tmp_min = time_paper.minute
                                    print(f'debug1: {flag_time_first_min}, {tmp_min}={time_paper.minute} ')

                                if tmp_min != time_paper.minute:
                                    flag_time_first_min = False
                                    cnt_reset = 0
                                    cnt_stop = 0
                                    print(f'debug2: {flag_time_first_min}, {tmp_min}={time_paper.minute} ')
                                    tmp_min = time_paper.minute

                                    # сохраняем последюню актуальную цену после закрытия сессии в 16-00 по Чикаго
                                    if time_paper.hour == 16 and time_paper.minute == 0:
                                        # self.contract_price_last = self.contract_price
                                        self.R_W_config(param="price_last", val=self.contract_price)

                            # else:
                            #     print("b")
                            print("f12")

                            # except Exception:
                            #     print(f'Ошибка в flag_time_paper (?)')
                            #     log_r.info(f'Ошибка в flag_time_paper (?)')
                            #     self.MessageInfo(f'Ошибка в flag_time_paper (?)')

                            # //////////////////// МЕДЛЕННЫЕ ЗАПРОСЫ. Начало ////////////////////

                            # !!! сюда надо именно время сервера
                            print("f13")
                            local_time = datetime.now()
                            try:
                                # self.mainwindow.lbl_server_time_Edit.setText(
                                #     str(local_time.strftime("%A, %d-%m-%Y, %H:%M:%S")))
                                self.set_FromRobotAppToQT(param="lbl_server_time_Edit",
                                                          text=str(local_time.strftime("%A, %d-%m-%Y, %H:%M:%S")))
                            except Exception as e:
                                print(f"Ошибка времени: {e}]")
                                logging.critical(f"Ошибка времени: {e}]")
                            print("f14")
                            # получаем время нашей бумаги
                            try:
                                if self.contract_tz != "non":
                                    # print(f'self.contract_tz 2 = {self.contract_tz}')
                                    time_paper = datetime.now(pytz.timezone(self.contract_tz))  # ('US/Central'))
                                    flag_time_paper = True  # day_old = time_paper.day  # сохраняем текущий день месяца
                                # self.mainwindow.lbl_working_time_Edit.setText(
                                #     str(time_paper.strftime("%A, %d-%m-%Y, %H:%M:%S")))
                                self.set_FromRobotAppToQT(param="lbl_working_time_Edit",
                                                          text=str(time_paper.strftime("%A, %d-%m-%Y, %H:%M:%S")))
                            except:
                                print(f"Проблемы c чтением бумаги - {self.contract_1['localSymbol']}")
                                logging.critical(f"Проблемы c чтением бумаги - {self.contract_1['localSymbol']}")
                                self.MessageInfo(f"Проблемы c чтением бумаги - {self.contract_1['localSymbol']}")
                                self.MessageInfo(f"Возможно {self.contract_1['localSymbol']} уже не торгуется или "
                                                 f"кончилась подписка на рыночные данные...")
                                self.mainwindow.button_Connect()  # принудительно вызываем Кнопку Disconnect
                                # self.ButtonConnectToQT.emit()  #"button_Connect")  # принудительно вызываем Кнопку Disconnect
                                self.cancelMktData(self.nextOrderId())
                                self.reqAccountUpdates(False, "")
                                self.flag_account_with_server = False

                            print("f15")
                            # анализируем 5-ти минутки
                            if self.flag_5_min_candle:
                                self.flag_5_min_candle = False

                                # if self.index_day_candle == 2:
                                # достаем время
                                time_tmp = float(self.day_candle[self.index_day_candle - 1]['dt'])
                                time_tmp_min = datetime.fromtimestamp(int(time_tmp)).astimezone(
                                    pytz.timezone(self.contract_tz)).minute
                                print('time_tmp', time_tmp, "time_tmp_min", time_tmp_min)
                                if time_tmp_min == int(self.time_to_act['input_min']):
                                    # Предолагаем, что последнняя свеча - это наша искомая
                                    self.price_input_trade = float(self.day_candle[self.index_day_candle - 1]['o'])
                                    self.R_W_config(param="price_input", val=self.price_input_trade)
                                    self.price_input_trade_avg = avgfillprice
                                    self.R_W_config(param="price_input_avg", val=self.price_input_trade_avg)
                                    # self.mainwindow.lbl_price_input_trade_Edit.setText(str(self.price_input_trade))
                                    self.set_FromRobotAppToQT(param="lbl_price_input_trade_Edit",
                                                              text=f"{format(self.price_input_trade_avg, '.2f')}")
                                    print("Средняя точка входа:", avgfillprice)
                                    tmp_str = str(f"Trade entry (account {self.account}):\n"
                                                  f"{datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}\n"
                                                  f"Paper: {self.contract_1['localSymbol']}\n"
                                                  f"Average Entry Point: {avgfillprice}\n"
                                                  f"Stop: {self.price_stop_trade}\n"
                                                  f"Position Size: {self.position} lot(s)\n")
                                    self.MessageEmail(subject=f"Trade entry (account {self.account})",
                                                      to_addr=self.to_addr_email,
                                                      text=tmp_str
                                                      )
                                    tB2.send(tmp_str)
                                else:
                                    cnt_reqHistoricalData = 0
                                    self.flag_read_5mins = True
                                    self.flag_contract_price_change = True

                            print("f16")
                            # если массив дневных свечек заполнены - считаем сессию и тренд
                            # эксперимент - что будет если во время нахождения в позе продолжать считать всякие параметры
                            if self.flag_day_candle and self.go > 0:  # and self.position == 0:  # или self.flag_Position ?
                                self.flag_day_candle = False
                                # вычисляем рабочую сессию
                                num_month = self.day_candle[self.NUM_DAY_CANDLE]['dt'][4:6]  # номер месяца текущего дня
                                work_session = 0
                                for i in range(self.NUM_DAY_CANDLE, 1, -1):
                                    num_month_tmp = self.day_candle[i]['dt'][4:6]
                                    if num_month_tmp == num_month:
                                        work_session += 1
                                    else:
                                        break
                                # на выходе получаем номер рабочей сессии
                                print("Рабочая сессия №", work_session)
                                # self.servicewindow.lbl_work_session_Edit.setText(str(work_session))
                                self.set_FromRobotAppToQT_srv(param="lbl_work_session_Edit", text=str(work_session))
                                # определяем направление захода
                                direction = self.tdm[str(work_session)]
                                if direction == "+L":  # если сегодня в лонг
                                    direction = "BUY"  # будем покупать
                                elif direction == "-L":  # если сегодня в шорт
                                    direction = "SELL"  # будем продавать
                                else:
                                    direction = "NONE"  # иначе ничего
                                print("Направление по календарю", direction)
                                # self.servicewindow.lbl_direction_Edit.setText('/') if direction == "BUY" else \
                                #     self.servicewindow.lbl_direction_Edit.setText('None')
                                self.set_FromRobotAppToQT_srv(param="lbl_direction_Edit", text='/') \
                                    if direction == "BUY" else self.set_FromRobotAppToQT_srv(param="lbl_direction_Edit",
                                                                                             text='None')

                                # определяем текущий день недели
                                week_day = time_paper.weekday()
                                print("День недели", dict_week_day[week_day])
                                # self.servicewindow.lbl_week_day_Edit.setText(dict_week_day[week_day])
                                self.set_FromRobotAppToQT_srv(param="lbl_week_day_Edit", text=dict_week_day[week_day])

                                # определяем тренд
                                trend = self.tdw[str(week_day)]
                                if trend > 23:  # проверка на дурака - в месяце не бывает более 23 рабочих дней
                                    pass  # раскомментировать  для работы trend = 23
                                delta = self.day_candle[self.NUM_DAY_CANDLE - 1]['c'] - \
                                        self.day_candle[self.NUM_DAY_CANDLE - 1 - trend]['c']
                                print("Дней в тренде", trend, ", дельта тренда", delta)
                                # self.servicewindow.lbl_days_in_trend_Edit.setText(str(trend))
                                self.set_FromRobotAppToQT_srv(param="lbl_days_in_trend_Edit", text=str(trend))
                                # self.servicewindow.lbl_trend_delta_Edit.setText(str(delta) + ' /') if delta >= 0 else \
                                #     self.servicewindow.lbl_trend_delta_Edit.setText(str(delta) + ' \\')
                                self.set_FromRobotAppToQT_srv(param="lbl_trend_delta_Edit", text=(str(delta) + ' /')) \
                                    if delta >= 0 else self.set_FromRobotAppToQT_srv(param="lbl_trend_delta_Edit",
                                                                                     text=(str(delta) + ' \\'))

                                # определим приказ
                                if direction == "BUY" and trend > 0 and delta >= self.delta_trend:
                                    self.order_direction = direction
                                elif direction == "SELL" and trend > 0 and delta <= -self.delta_trend:
                                    self.order_direction = direction
                                else:
                                    self.order_direction = "None"
                                print("ПреПриказ", self.order_direction)
                                # self.servicewindow.lbl_order_direction_Edit.setText(str(self.order_direction))
                                self.set_FromRobotAppToQT_srv(param="lbl_order_direction_Edit",
                                                              text=str(self.order_direction))
                                if self.position == 0:
                                    self.set_FromRobotAppToQT(param="lbl_order_direction_Edit",
                                                              text=str(self.order_direction))
                                else:
                                    self.set_FromRobotAppToQT(param="lbl_order_direction_Edit",
                                                              text="None")

                                # определяем величину стопа
                                summa = 0
                                volat_day = 0
                                svv = 0
                                for i in range(self.NUM_DAY_CANDLE - 1, self.NUM_DAY_CANDLE - 1 - self.svv_day, -1):
                                    volat_day = self.day_candle[i]['h'] - self.day_candle[i]['l']
                                    summa += volat_day
                                svv = summa / self.svv_day
                                print(f'СВВ({self.svv_day}) = {svv}')
                                relative_stop = (svv * self.stop_percent) / 100
                                print(f'Относительный стоп = {relative_stop}')
                                relative_stop = roundTick(cena=relative_stop, tick=self.minTick,
                                                          param="+")  # стоп округляем в большую сторону
                                print(f'Относительный стоп округлённый = {relative_stop}')

                                # self.servicewindow.lbl_svv_Edit.setText(str(round(svv, 2)))
                                self.set_FromRobotAppToQT_srv(param="lbl_svv_Edit", text=str(round(svv, 2)))
                                # !!!!! стересть дебаг
                                # order_direction = "BUY"
                                # абсолютный стоп = открытие дня +- относительный стоп
                                if self.order_direction == "BUY":  # если покупаем - стоп будем ставить ниже
                                    absolute_stop = (self.day_candle[self.NUM_DAY_CANDLE]['o'] - relative_stop)
                                elif self.order_direction == "SELL":  # если продаем - стоп будем ставить выше
                                    absolute_stop = (self.day_candle[self.NUM_DAY_CANDLE]['o'] + relative_stop)
                                else:
                                    absolute_stop = 0
                                print(f'Абсолютный стоп = {absolute_stop}')
                                # self.servicewindow.lbl_absolute_stop_Edit.setText(str(absolute_stop))
                                self.set_FromRobotAppToQT_srv(param="lbl_absolute_stop_Edit", text=str(absolute_stop))

                                # Проверка - а не ушла ли цена за пределы стопа? - заходить не будем если так
                                if self.order_direction == "BUY":
                                    # если нам в лонг и текущая цена ниже стопа (чуть ухудшаем текущую цену)
                                    if absolute_stop >= (self.contract_price - (4 * self.minTick)):
                                        self.order_direction = "None"
                                        print("Цена возле стопа или ниже: стоп =", absolute_stop, ", цена = ",
                                              (self.contract_price - (4 * self.minTick)), ", сброс приказа в",
                                              self.order_direction)

                                if self.order_direction == "SELL":
                                    # если нам в шорт и текущая цена выше стопа (чуть ухудшаем текущую цену)
                                    if absolute_stop <= (self.contract_price + (4 * self.minTick)):
                                        self.order_direction = "None"
                                        print("Цена возле стопа или выше: стоп =", absolute_stop, ", цена = ",
                                              (self.contract_price - (4 * self.minTick)), ", сброс приказа в",
                                              self.order_direction)

                                # Вычисляем на сколько будем заходить в зависимости от риска
                                # считаем сколько потеряем в баксах одним лотом
                                if self.order_direction != "None" and absolute_stop > 0:
                                    loss_1_lot = abs(absolute_stop - self.contract_price) * self.pip_price
                                elif self.order_direction == "None":
                                    loss_1_lot = relative_stop * self.pip_price
                                else:
                                    loss_1_lot = 0
                                relative_stop_curr = (
                                    abs(absolute_stop - self.contract_price)) if absolute_stop != 0 else 0
                                print(f'Относительный стоп текущий = {relative_stop_curr}')
                                print(
                                    f'Потеря на один лот = {loss_1_lot}')  # (({absolute_stop}-{self.contract_price})*{self.pip_price})')
                                # self.servicewindow.lbl_relative_stop_Edit.setText(str(relative_stop) + ' (' +
                                #                                                   str(relative_stop_curr) + ')')
                                self.set_FromRobotAppToQT_srv(param="lbl_relative_stop_Edit",
                                                              text=str(relative_stop) + ' (' + str(
                                                                  relative_stop_curr) + ')')

                                # self.servicewindow.lbl_loss_1_lot_Edit.setText(f'{loss_1_lot} {self.currency_account}')
                                self.set_FromRobotAppToQT_srv(param="lbl_loss_1_lot_Edit",
                                                              text=f'{loss_1_lot} {self.currency_account}')

                                # считаем - сколько готовы потерять исходя из риска и нашего депозита
                                abs_loss_1_trade = (self.free_money * self.risk) / 100
                                print(f'При риске {self.risk}% из {self.free_money} готовы потерять {abs_loss_1_trade}')
                                # self.servicewindow.lbl_abs_loss_1_trade_Edit.setText(f'{round(abs_loss_1_trade, 2)} '
                                #                                                      f'{self.currency_account} '
                                #                                                      f'({self.risk}%)')
                                self.set_FromRobotAppToQT_srv(param="lbl_abs_loss_1_trade_Edit",
                                                              text=f'{round(abs_loss_1_trade, 2)} '
                                                                   f'{self.currency_account} '
                                                                   f'({self.risk}%)')

                                # Т.о. размер входа в лотах составляет
                                number_of_lot = int(abs_loss_1_trade // loss_1_lot) if loss_1_lot != 0 else 0
                                # print(f'Будем заходить на {number_of_lot} лотов')
                                # # self.servicewindow.lbl_number_of_lot_Edit.setText(str(number_of_lot))
                                # self.set_FromRobotAppToQT_srv(param="lbl_number_of_lot_Edit", text=str(number_of_lot))

                                # рассчитаем минимальный депозит
                                if self.risk > 0:
                                    # минимальный депозит + немного увеличиваем минимальный депозит на 2%
                                    min_depo = ((loss_1_lot * 100) / self.risk) * 1.02 if self.risk != 0 else 0  #
                                    print(f"min_depo={min_depo}, loss_1_lot={loss_1_lot}, self.risk={self.risk}"
                                          f"self.go={self.go} ")
                                    if min_depo < (self.go * 1.02):
                                        min_depo = round((self.go * 1.02), 2)
                                        number_of_lot = 0
                                else:
                                    min_depo = 0
                                    number_of_lot = 0

                                if not flag_number_of_lot_0 and number_of_lot == 0:
                                    flag_number_of_lot_0 = True
                                    self.MessageInfo(f"Для входа в сделку денег на депозите не достаточно. "
                                                     f"Необходимо не менее {min_depo} {self.currency_account} (оценочно)")

                                print(f'Будем заходить на {number_of_lot} лотов')
                                # self.servicewindow.lbl_number_of_lot_Edit.setText(str(number_of_lot))
                                self.set_FromRobotAppToQT_srv(param="lbl_number_of_lot_Edit",
                                                              text=str(number_of_lot))

                                print(f'Оценочный минимальный депозит равен {round(min_depo, 2)}')
                                # self.mainwindow.lbl_min_depo_Edit.setText(f'{min_depo} {self.currency_account}')
                                self.set_FromRobotAppToQT(param="lbl_min_depo_Edit",
                                                          text=f'{min_depo} {self.currency_account}')

                            print("f17")
                            # если изменилась цена контракта
                            if self.flag_contract_price_change:
                                self.flag_contract_price_change = False
                                # self.mainwindow.lbl_paper_price_Edit.setText(str(self.contract_price)) float('{:.2f}'.format(self.contract_price))
                                # if self.contract_price is not None:
                                self.set_FromRobotAppToQT(param="lbl_paper_price_Edit",
                                                          text=f"{format(self.contract_price, '.2f')}")
                                # else:
                                #     self.set_FromRobotAppToQT(param="lbl_paper_price_Edit",
                                #                               text=f"{format(self.contract_price_last, '.2f')}")
                                #     self.contract_price = self.contract_price_last
                                # print(f"price - {format(self.contract_price,'.3f')}")
                                # запросим данные по свечам (будем заказывать с периодом 10)
                                if cnt_reqHistoricalData == 0:
                                    cnt_reqHistoricalData = 10
                                    if self.flag_read_5mins:  # если надо прочитать пятиминутки
                                        self.reqHistoricalData(self.nextOrderId(), contract, "",
                                                               "100 S", "5 mins", "TRADES", 0, 2, False, [])  # 1 min
                                    # else:  # иначе читаем дни
                                    #     self.reqHistoricalData(self.nextOrderId(), contract, "",
                                    #                            str(self.NUM_DAY_CANDLE) + " D",
                                    #                            "1 day", "TRADES", 0, 1, False, [])

                                    self.index_day_candle = 1
                                    self.Trade(contract=contract, trd="INPUT",
                                               order_direction=self.order_direction if self.order_direction != "None" else "BUY",
                                               position=1, contract_price=self.contract_price,
                                               orderType="LMT", real="demo")

                                cnt_reqHistoricalData -= 1

                                # будем читать дневные свечи раз в минуту
                                if trig_reqHistory != time_paper.minute:
                                    trig_reqHistory = time_paper.minute
                                    self.reqHistoricalData(self.nextOrderId(), contract, "",
                                                           str(self.NUM_DAY_CANDLE) + " D",
                                                           "1 day", "TRADES", 0, 1, False, [])
                                    self.index_day_candle = 1

                            print("f18")
                            # если произошло изменение в размере счета
                            if self.flag_NetLiquidation_change:
                                self.flag_NetLiquidation_change = False
                                # self.mainwindow.lbl_account_size_Edit.setText(self.NetLiquidation)
                                self.set_FromRobotAppToQT(param="lbl_account_size_Edit", text=self.NetLiquidation)
                                # self.mainwindow.lbl_available_funds_Edit.setText(self.AvailableFunds)
                                self.set_FromRobotAppToQT(param="lbl_available_funds_Edit", text=self.AvailableFunds)
                                # self.servicewindow.lbl_available_funds_Edit.setText(self.AvailableFunds)
                                self.set_FromRobotAppToQT_srv(param="lbl_available_funds_Edit",
                                                              text=self.AvailableFunds)

                            print("f19")
                            # если произошло изменение в позиции
                            if self.flag_position_change:
                                self.flag_position_change = False
                                # self.mainwindow.lbl_position_size_Edit.setText(str(self.position))
                                self.set_FromRobotAppToQT(param="lbl_position_size_Edit", text=str(self.position))
                                if self.position > 0:
                                    order_direction_view = "BUY"
                                    # self.mainwindow.lbl_direction_Edit.setStyleSheet("QLabel {color:green}")
                                elif self.position < 0:
                                    order_direction_view = "SELL"
                                    # self.mainwindow.lbl_direction_Edit.setStyleSheet("QLabel {color:red}")
                                else:
                                    order_direction_view = "-"
                                    # self.mainwindow.lbl_direction_Edit.setStyleSheet("QLabel {color:black}")
                                # self.mainwindow.lbl_direction_Edit.setText(order_direction_view)
                                self.set_FromRobotAppToQT(param="lbl_direction_Edit", text=order_direction_view)

                                if self.position != 0:
                                    # self.mainwindow.lbl_robot_state_Edit.setText("In position")
                                    self.set_FromRobotAppToQT(param="lbl_robot_state_Edit", text="In position")
                                    self.flag_Position = True

                                    # self.mainwindow.lbl_robot_state_Edit.setStyleSheet("color: green")
                                else:
                                    # self.mainwindow.lbl_robot_state_Edit.setText("Out of position")
                                    self.set_FromRobotAppToQT(param="lbl_robot_state_Edit", text="Out of position")
                                    self.flag_Position = False
                                    flag_need_output = False

                                    # self.mainwindow.lbl_robot_state_Edit.setStyleSheet("color: red")

                                # просто здесь поставим вывод - точки входа, и стопа - Иногда
                                # self.mainwindow.lbl_price_input_trade_Edit.setText(str(self.price_input_trade))
                                self.set_FromRobotAppToQT(param="lbl_price_input_trade_Edit",
                                                          text=f"{format(self.price_input_trade_avg, '.2f')}")
                                # self.mainwindow.lbl_price_stop_trade_Edit.setText(str(self.price_stop_trade))
                                self.set_FromRobotAppToQT(param="lbl_price_stop_trade_Edit",
                                                          text=f"{format(self.price_stop_trade, '.2f')}")
                            print("f111")
                            # если сделка совершена - либо отказы
                            if self.flag_execDetails:  # сделка совершена на кол-во лотов  = execution.shares
                                self.flag_execDetails = False
                                logging.info(f'Trade: {self.param_execDetails["execution"].shares} contract(s), '
                                             f'Contract: {self.param_execDetails["contract"].localSymbol}')
                                self.MessageInfo(f'Trade: {self.param_execDetails["execution"].shares} contract(s), '
                                                 f'Contract: {self.param_execDetails["contract"].localSymbol}')
                            print("f112")
                            if self.flag_orderStatus:
                                self.flag_orderStatus = False
                                logging.info(f'OrderStatus: {self.param_orderStatus["status"]}, '
                                             f'Filled: {self.param_orderStatus["filled"]}, '
                                             f'Remaining: {self.param_orderStatus["remaining"]}, '
                                             f'LastFillPrice: {self.param_orderStatus["lastFillPrice"]}')
                                # self.MessageInfo(f'OrderStatus: {self.param_orderStatus["status"]}, '
                                #                  f'Filled: {self.param_orderStatus["filled"]}, '
                                #                  f'Remaining: {self.param_orderStatus["remaining"]}, '
                                #                  f'LastFillPrice: {self.param_orderStatus["lastFillPrice"]}')

                                # если полностью закрыли сделку - пишем это
                                if self.param_orderStatus["status"] == "Filled" and self.param_orderStatus[
                                    "remaining"] == 0:
                                    logging.critical(
                                        f'Сделка на {self.param_orderStatus["filled"]} контракт(ов) завершена!')
                                    self.MessageInfo(
                                        f'Сделка на {self.param_orderStatus["filled"]} контракт(ов) завершена!')
                                    print(f'Сделка на {self.param_orderStatus["filled"]} контракт(ов) завершена!')
                                    contract_subtractor = 0
                                    avgfillprice = self.param_orderStatus["avgFillPrice"]
                                    logging.critical(
                                        f'debug1: str_orderStatus: {self.str_orderStatus}')
                                    logging.critical(
                                        f'debug2: param_orderStatus: {self.param_orderStatus}')

                                    # если полностью закрыли сделку после входа в позу - формируем стоп
                                    if flag_input:
                                        self.flag_Position = True
                                        flag_one_trade = False
                                        flag_input = False
                                        # формируем стоп
                                        if self.order_direction == "BUY":
                                            order_direction_stop = "SELL"
                                        elif self.order_direction == "SELL":
                                            order_direction_stop = "BUY"

                                        order.action = order_direction_stop
                                        order.totalQuantity = self.param_orderStatus["filled"]
                                        order.orderType = "STP"
                                        order.auxPrice = absolute_stop
                                        order.tif = "GTC"
                                        order.outsideRth = True  # - что бы ордер срабатывал вне обычных торговых часов
                                        # self.simplePlaceOid = self.nextOrderId()
                                        self.placeOrder(self.nextOrderId(), contract, order)
                                        # print("self.simplePlaceOid = ", self.simplePlaceOid)
                                        self.price_stop_trade = absolute_stop
                                        self.R_W_config(param="price_stop", val=self.price_stop_trade)
                                        # self.mainwindow.lbl_price_stop_trade_Edit.setText(str(self.price_stop_trade))
                                        self.set_FromRobotAppToQT(param="lbl_price_stop_trade_Edit",
                                                                  text=f"{format(self.price_stop_trade, '.2f')}")
                                        # запрос параметров текущей свечи - для определения ориентировочной точки входа
                                        # для этого обнулим счетчик чтений свечек - чтобы читал по принуждению
                                        cnt_reqHistoricalData = 0
                                        self.flag_read_5mins = True
                                        self.flag_contract_price_change = True

                                    # если было срабатывание стопа
                                    if (self.param_openOrder["order"].orderType == "STP" or
                                        self.param_openOrder["order"].orderType == "STP LTM") and \
                                            self.param_openOrder["orderState"].status == "Filled":
                                        # self.flag_openOrderEnd = True  # альтернатива self.reqOpenOrders()
                                        flag_output = True
                                        exit_reason = "Stop"
                                        print("Сработал стоп")
                                        self.MessageInfo("Сработал стоп")
                                        logging.critical("Сработал стоп")

                                    # если полностью закрыли сделку после выхода из позы - убираем все заявки
                                    if flag_output:
                                        self.flag_Position = False
                                        flag_one_trade = False

                                        # считаем кол-во стопов в 1 минуту - если они были
                                        if flag_time_first_min:
                                            cnt_stop += 1

                                            # flag_output = False
                                        # self.reqGlobalCancel() # снимаем все ордера
                                        # self.cancelOrder(self.simplePlaceOid, "") # снимаем конкретный ордер
                                        self.reqOpenOrders()  # если у нас было срабатывание по стопу
                                        # то у этой функции ответа не будет

                                        print(f"Выход из сделки по цене {self.contract_price}")
                                        tmp_str = str(f"Trade exit (account {self.account}):\n"
                                                      f"{datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}\n"
                                                      f"Paper: {self.contract_1['localSymbol']}\n"
                                                      f"Average exit point: {avgfillprice}\n"
                                                      f"Closed position size: {self.param_orderStatus['filled']} "
                                                      f"lot(s)\n"
                                                      f"Exit reason: {exit_reason}")
                                        self.MessageEmail(subject=f"Trade exit (account {self.account})",
                                                          to_addr=self.to_addr_email,
                                                          text=tmp_str)
                                        tB2.send(tmp_str)
                                        exit_reason = "None"
                                        # при срабатывании стопа - reqOpenOrders() - ничего не вернет
                                        # следовательно мы не пойдем делать self.flag_openOrderEnd = False
                                        # и flag_output = False - и не обнулим конфиг
                                        # надо здесь определять что был именно Стоп и обнулять кнфиг
                                        # и делать flag_output = False
                            print("f113")
                            if self.flag_openOrderEnd:
                                self.flag_openOrderEnd = False

                                # закрываем стопы после выхода из позы
                                if flag_output:
                                    flag_output = False
                                    print('Хотим снимать заявки/стопы')
                                    if (self.param_openOrder["order"].clientId == self.client_id) and \
                                            (self.param_openOrder["order"].orderType == "STP" or \
                                             self.param_openOrder["order"].orderType == "STP LTM"):
                                        print(f'Снимаем заявку/стопы: {self.param_openOrder}')
                                        self.cancelOrder(self.param_openOrder["orderId"], "")
                                        # self.order_direction = "None"
                                        self.price_input_trade_avg = 0
                                        self.price_input_trade = 0
                                        self.price_stop_trade = 0
                                        self.R_W_config(param="price_stop", val=self.price_stop_trade)
                                        self.R_W_config(param="price_input", val=self.price_input_trade)
                                        self.R_W_config(param="price_input_avg", val=self.price_input_trade_avg)
                                        # self.mainwindow.lbl_price_input_trade_Edit.setText(str(self.price_input_trade))
                                        self.set_FromRobotAppToQT(param="lbl_price_input_trade_Edit",
                                                                  text=f"{format(self.price_input_trade_avg, '.2f')}")
                                        # self.mainwindow.lbl_price_stop_trade_Edit.setText(str(self.price_stop_trade))
                                        self.set_FromRobotAppToQT(param="lbl_price_stop_trade_Edit",
                                                                  text=f"{format(self.price_stop_trade, '.2f')}")
                                        # self.R_W_config(param="direction", val=self.order_direction)

                                    # если выходили по Сбросу - делаем дисконнект
                                    if self.flag_reset:
                                        self.mainwindow.button_Connect()
                                        # self.ButtonConnectToQT.emit()  #"button_Connect")  # делаем дисконнект

                            # если заявку отклонили + ошибка: Поставили много контрактов
                            print("f114")
                            if self.flag_error_message:
                                self.flag_error_message = False
                                logging.critical(self.message_error)
                                # self.MessageInfo(self.message_error)

                                if self.flag_error_201:
                                    if self.param_orderStatus["status"] == "Inactive":
                                        self.flag_error_201 = False
                                        # то будем выставлять заново - уменьшив количество контрактов
                                        flag_one_trade = False
                                        contract_subtractor += 1

                                if self.flag_error_460:
                                    self.flag_error_460 = False
                                    if not flag_error_460_1:
                                        flag_error_460_1 = True
                                        self.MessageInfo(
                                            'No trading permissions: (Account Management > Trading Permissions)')
                                        self.set_FromRobotAppToQT_srv(param="lbl_go_Edit",
                                                                      text=f'No trading permissions')

                            print("f115")
                            if self.flag_openOrder:
                                self.flag_openOrder = False
                                logging.info(f'OpenOrder: {self.param_openOrder["order"].action}, '
                                             f'Status: {self.param_openOrder["orderState"].status}')
                                # self.servicewindow.lbl_go_Edit.setText(f'{round(self.go, 2)} {self.currency_account}')
                                self.set_FromRobotAppToQT_srv(param="lbl_go_Edit",
                                                              text=f'{round(self.go, 2)} {self.currency_account}')
                                # self.MessageInfo(f'OpenOrder: {self.param_openOrder["order"].action}, '
                                #                  f'Status: {self.param_openOrder["orderState"].status}')
                                # print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange,
                                #       ":",
                                #       order.action, order.orderType, order.totalQuantity, orderState.status)
                                # self.param_openOrder = {'contract': contract, 'order': order, 'orderState': orderState}
                            print("f116")
                            if self.flag_contractDetails:
                                self.flag_contractDetails = False
                                # если у нас в конфиге нет даты последнего дня торговли
                                # if self.lastTradeDate == "":
                                # если дата прочитанного контракта не равна дате в конфиге - перезапишем
                                if self.contract_details.contract.lastTradeDateOrContractMonth != self.lastTradeDate:
                                    self.R_W_config(param='lastTradeDate',
                                                    val=self.contract_details.contract.lastTradeDateOrContractMonth)

                                tmp_str = self.contract_details.contract.lastTradeDateOrContractMonth
                                self.MessageInfo(
                                    f"Последний торговый день бумаги {self.contract_1['localSymbol']} - {tmp_str[6:8]}.{tmp_str[4:6]}.{tmp_str[0:4]}")

                            print("f117")
                            # смена дня
                            if time_paper.day != day_old:
                                print(f'Смена дня day_old={day_old}, time_paper.day={time_paper.day}')
                                day_old = time_paper.day
                                # напоминание об окончании фьючерса
                                now = time_paper.date()
                                then = datetime(int(self.lastTradeDate[0:4]), int(self.lastTradeDate[4:6]),
                                                int(self.lastTradeDate[6:8])).date()
                                delta_d = then - now
                                print(f'Кол-во дней до смены фьючерса delta_d: {delta_d.days} = {then} - {now}')
                                # if delta_d.days <= 89:
                                print(f'До смены бумаги осталось: {delta_d.days} day(s)')
                                logging.critical(f'До смены бумаги осталось: {delta_d.days} day(s)')
                                self.MessageInfo(f'До смены бумаги осталось: {delta_d.days} day(s)')

                                week_day = time_paper.weekday()
                                print(f"День недели - {week_day} - {dict_week_day[week_day]}")

                        # //////////////////// МЕДЛЕННЫЕ ЗАПРОСЫ. Конец ////////////////////

                        # Конец - if flag_account_true: # если аккаунт валидный
                        print("f2")
                        # проверка аккаунта на валидность
                        if self.flag_account_with_server and (not flag_account_true):
                            # если номер аккаунта прочитан с сервера - сверяем
                            logging.critical('-------------- Новая Сессия ---------------')
                            self.MessageInfo('-------------- Новая Сессия ---------------')
                            resvalacc_account = resvalacc(self.account)
                            try:
                                t = self.mos_list.index(resvalacc_account)  # (self.account)
                                print(f'Аккаунт подтвержден: {self.account} is valid')
                                logging.info(f'Аккаунт подтвержден: {self.account} is valid')
                                self.MessageInfo(f'Аккаунт подтвержден: {self.account} is valid')
                                # self.mainwindow.lbl_account_Edit.setText(self.account)
                                self.set_FromRobotAppToQT(param="lbl_account_Edit", text=self.account)
                                flag_account_true = True
                                self.flag_account_with_server = False
                            except ValueError:
                                print(f'Неизвестный аккаунт: {self.account} is not valid')
                                logging.info(f'Неизвестный аккаунт: {self.account} is not valid')
                                self.MessageInfo(f'Неизвестный аккаунт: {self.account} is not valid')
                                self.mainwindow.button_Connect()  # принудительно вызываем Кнопку Disconnect
                                # self.ButtonConnectToQT.emit()  #"button_Connect")
                                self.cancelMktData(self.nextOrderId())
                                self.reqAccountUpdates(False, "")
                                self.flag_account_with_server = False

                        print("f3")
                        # Сброс робота
                        if self.servicewindow.flag_reset:  # and not flag_one_trade:
                            self.servicewindow.flag_reset = False
                            # self.set_FromRobotAppToQT_srv(param="flag_reset", text="False")
                            # self.signals_FromRobotAppToQT_srv["flag_reset"] = "None" # сброс флага

                            if flag_time_first_min:
                                cnt_reset += 1

                            print(f'Сброс робота...')
                            logging.info(f'Сброс робота...')
                            self.MessageInfo(f'Сброс робота...')

                            self.flag_reset = True
                            # flag_one_trade = True
                            # print("Нажали Сброс робота")
                            # закрываем позы если есть
                            if self.flag_Position:  # and not flag_one_trade:
                                print("Нажали Сброс робота, когда мы в сделке")
                                self.Trade(contract=contract, trd="OUTPUT", position=self.position,
                                           contract_price=self.contract_price, orderType="LMT")
                                # закрываем стопы если есть
                                flag_output = True
                                exit_reason = "Robot Reset"

                            else:  # if not self.flag_Position:
                                print("Нажали Сброс робота, когда мы не в сделке")
                                self.price_input_trade_avg = 0
                                self.price_input_trade = 0
                                self.price_stop_trade = 0
                                self.R_W_config(param="price_stop", val=self.price_stop_trade)
                                self.R_W_config(param="price_input", val=self.price_input_trade)
                                self.R_W_config(param="price_input_avg", val=self.price_input_trade_avg)
                                # self.mainwindow.lbl_price_input_trade_Edit.setText(str(self.price_input_trade))
                                self.set_FromRobotAppToQT(param="lbl_price_input_trade_Edit",
                                                          text=f"{format(self.price_input_trade_avg, '.2f')}")
                                # self.mainwindow.lbl_price_stop_trade_Edit.setText(str(self.price_stop_trade))
                                self.set_FromRobotAppToQT(param="lbl_price_stop_trade_Edit",
                                                          text=f"{format(self.price_stop_trade, '.2f')}")
                                # self.R_W_config(param="direction", val=self.order_direction)
                                self.mainwindow.button_Connect()  # делаем дисконнект
                                # self.ButtonConnectToQT.emit()  #"button_Connect")
                                # print(f"флаг2 flag_connect {self.mainwindow.flag_connect}")
                                break

                        print("f4")
                        # нажали кнопку закрытия робота - будем рассоединяться
                        # в сам closeEvent добавил lag_connect=false => в этот if мы не должны захаодить
                        # if self.mainwindow.close_app:
                        #     print('Закрыли Интерфейс3')
                        #     logging.critical('Закрыли Интерфейс3')
                        #     self.cancelMktData(self.nextOrderId())
                        #     self.reqAccountUpdates(False, "")
                        #     # self.mainwindow.flag_connect = False
                        #     # self.mainwindow.button_Connect()  # делаем дисконнект
                        #     self.ButtonConnectToQT.emit("button_Connect")
                        #     # self.email.flag_run_email = False  # останавливаем поток почты
                        #     # self.telegram.flag_run_telegram = False  # останавливаем поток телеграмма -
                        #     # self.telegram_interactive.bot.close()  # .stop_bot()
                        #     # self.telegram_interactive.flag_run_telegram = False  # останавливаем поток телеграмма
                        #     break

                        print("f5")
                        # если нажали Disconnect
                        try:
                            if not self.mainwindow.flag_connect:
                                print('Нажали Disconnect')
                                logging.critical('Нажали Disconnect')
                                self.cancelMktData(self.nextOrderId())
                                self.reqAccountUpdates(False, "")
                                # self.mainwindow.lbl_account_Edit.setText("-")
                                self.set_FromRobotAppToQT(param="lbl_account_Edit", text="-")
                                self.MessageInfo('---------Связь с сервером прервана---------')
                                break
                        except Exception as e:
                            print(f"Ошибка flag_connect: {e}")
                            logging.critical(f"Ошибка flag_connect: {e}")
                        print("f6")
                except Exception as e:
                    print(f"Ошибка обработки сообщений: {e}")
                    logging.critical(f"Ошибка обработки сообщений: {e}")
                    # здесь надо делать дисконнект

                    # Заплатка от проблемы "9-06" - делаем переКоннект
                    self.mainwindow.button_Connect()  # делаем дисконнект
                    # self.ButtonConnectToQT.emit()  #"button_Connect")
                    self.flag_reset = True  # а затем этот флаг нам опять просто включит Коннект
                    flag_error_connect = True
                    time.sleep(2)
                # finally:
                print('Disconnect после закрытия окна')

                logging.info('Нажали Disconnect')
                # self.disconnect()
                # self.connectionClosed()




            # иначе если нажали на Disconnect - разъединяемся с сервером
            elif not self.mainwindow.flag_connect and flag_flag_connect_old:
                print('Разъединение после Disconnect 1')
                logging.info('Разъединение после Disconnect')
                # self.connectionClosed()
                try:
                    self.reqAccountUpdates(False, "")
                    # flag_flag_connect_old = False
                    # self.flag_read_config = False
                    # self.flag_read_calendar = False
                    # self.flag_read_mos = False
                    self.disconnect()
                except:
                    print('Нажали Disconnect, хоть мы и не были подсоединены.')

                flag_flag_connect_old = False
                self.flag_read_config = False
                self.flag_read_calendar = False
                self.flag_read_mos = False
                # self.mainwindow.lbl_server_conn_Edit.setText('NO')
                self.set_FromRobotAppToQT(param="lbl_server_conn_Edit", text="NO")

                time.sleep(1)

            # нажали кнопку закрытия робота - будем рассоединяться
            elif self.mainwindow.close_app:
                print('Закрыли Интерфейс 6')
                logging.info('Закрыли Интерфейс 6')
                # self.cancelMktData(self.nextOrderId())
                # self.reqAccountUpdates(False, "")
                self.email.flag_run_email = False  # останавливаем поток почты
                # self.telegram.flag_run_telegram = False  # останавливаем НЕинтерактивный телеграм
                # self.telegram_interactive.flag_run_telegram = False  # останавливаем Интерактивный телеграм
                # self.telegram_interactive.bot.stop_polling()         # останавливаем Интерактивный телеграм
                # tB1.flag_run_telegram = False  # останавливаем НЕинтерактивный телеграм
                tB2.flag_run_telegram = False  # останавливаем Интерактивный телеграм
                tB2.bot.stop_polling()  # останавливаем Интерактивный телеграм

                break

            # мы разъединены c сервером
            else:
                # пока не соединены с сервером читаем конфиг, либо перечитываем после изменения
                if (not self.flag_read_config) or self.servicewindow.flag_change_config:
                    flag_correct_config = self.ReadConfig()
                    self.servicewindow.flag_change_config = False
                    # self.set_FromRobotAppToQT_srv(param="flag_change_config", text="False")
                    # self.signals_FromRobotAppToQT_srv["flag_change_config"] = "None"  # сброс флага
                    day_old = 0
                    trig_reqHistory = 1000

                    if flag_correct_config and (not flag_create_telegram):
                        flag_create_telegram = True
                        # tB1 = robot_telebot.TelegramBot(interactive="non_interactive", token=self.telegram_token,
                        #                                 id=self.telegram_id)
                        tB2 = robot_telebot.TelegramBot(interactive="interactive", token=self.telegram_token,
                                                        id=self.telegram_id)
                        if tB2.flag_token_correct:  # если в телеграм токене хоть что-то есть
                            # - запускаем телеграм
                            # tB1.start()
                            tB2.start()
                            self.MessageInfo(f"Телеграм Бот проинициализирован")
                        else:
                            self.MessageInfo(f"Телеграм Бот не проинициализирован")

                    elif flag_create_telegram and self.telegram_token == "":
                        tB2.flag_run_telegram = False  # останавливаем Интерактивный телеграм
                        tB2.bot.stop_polling()  # останавливаем Интерактивный телеграм
                        tB2.bot.stop_bot()
                        print("Останавливаем телеграм-бота")

                if flag_correct_config:  # если конфиг корректен
                    # print(datetime.fromtimestamp().strftime("%Y%B%d"))
                    # print(self.contract_1['lastTradeDate'])

                    if tB2.flag_token_correct:  # если токен корректен
                        if tB2.flag_id:  # если был запрос id
                            tB2.flag_id = False
                            # записываем ID в конфиг
                            self.R_W_config(param="Telegram_id", val=str(tB2.id))
                            # tB1.id = tB2.id  # и передаем этот ID в НЕинтерактивный телеграм

                if not self.flag_read_calendar:
                    flag_correct_calendar = self.ReadCalendar()

                if not self.flag_read_mos:
                    flag_correct_mos = self.ReadMOS()

                a = a + 1
                print('a = ', a)
                print(self.mainwindow.flag_connect, ' ', flag_flag_connect_old)
                self.set_FromRobotAppToQT(param="empty", text="0")
                time.sleep(0.5)

                if self.flag_reset:
                    self.flag_reset = False
                    print(f'Произведен сброс робота')
                    logging.info(f'Произведен сброс робота')
                    if not flag_error_connect:
                        self.MessageInfo(f'Произведен сброс робота')
                        tB2.send(f"Reset robot - {datetime.now().strftime('%A, %d-%m-%Y, %H:%M:%S')}")

                    self.mainwindow.button_Connect()  # включили коннект
                    # self.ButtonConnectToQT.emit()  #"button_Connect")
                    # flag_one_trade = False
