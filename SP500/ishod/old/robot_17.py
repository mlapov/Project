"""
работает подсоединение с сервером
коннект и доисконнект корректны
Пара =  файл robot_5 + Interface_5

 к выяснению и доработке
  - если долго стоит работает - вылетает робот  - Process finished with exit code -1073740940 (0xC0000374)
    надо выяснить ошибку - так понимаю - ошибка с памятью связана - может многопоточность

  - что с летним/зимнем временем - pytz переключит ли?

  - наблюдал - TWS хочет перезагружаться сам в 23-45, в это время работал робот - в 23-45 - коннект пропал
  робот вылетел с сообщением Disconnect после закрытия окна и Process finished with exit code -1073740791 (0xC0000409)
  2022-07-20 23:45:31,696 - robot - INFO - Нажали Disconnect
  2022-07-20 23:45:31,696 - robot - INFO - Зашли во внешний цикл робота


  - выводить время сервера - сейчас просто локальное время - проблема - можно каждый раз запрашивать -
  время сервера - но это через чур большое кол-во запросов; можно выводить через например каждый 10 раз;
  можно синхронизировать текуе часы робота и серверные - пробовал - но это гемор

  - что если контракт не тот - уже старый

  - лицензия - файл mos.json - это по сути номер аккаунта - его надо будет читать наверное из файла какого-то - шифрованная запись

    - вылетает - прпробывать оградить обращение к интерфейсу - mainwindow от потока RobotApp,
    применить блокировки, и не обращаться в функциях обработки сообщений к mainwindow

    - если в позе в TWS и запускаем робота  - выбрасывает

    - если пихаю Log_r в функции типа orderStatus, openOrder - обработчики прерываний - выскакивают варнинги

    - причина вылетов time_paper - иногда может  быть не корректен - неизвестного типа
"""
import json
import logging
import os
import sys
from threading import Thread
import time
from datetime import datetime

import pytz
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame)

from PyQt5.QtCore import QCoreApplication, Qt, QThread, QMutex
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
from ibapi.utils import (current_fn_name, BadMessage)
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

if not os.path.exists("log"):
    os.makedirs("log")

log_r = logging.getLogger('robot')
log_r.setLevel(logging.INFO)
fh = logging.FileHandler("log/robot.log", 'a', 'utf-8')  # каждый раз новый файл 'w', дозапись 'a'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log_r.addHandler(fh)

import Interface


class RobotApp(QThread, EWrapper, EClient):
    def __init__(self, mainwindow, servicewindow, *args, **kwargs):
        EClient.__init__(self, self)
        super(RobotApp, self).__init__(*args, **kwargs)

        self.flag_error_message = False
        self.nextValidOrderId = 1
        self.flag_error_201 = False
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
        self._mutex = QMutex()
        self.server_time = None
        self.contract_1 = {}
        self.contract_tz = "non"
        self.flag_Position = False  # мы в позе True, мы не в позе False
        self.tdw = {}
        self.tdm = {}

        # QThread.daemon = True  # выключает поток при закрытии интерфейса

    # def connectionClosed(self):
    #     print('46')
    #     EClient.disconnect()

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
        # self.mainwindow.lbl_server_time_Edit.setText(str(self.server_time))

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        # self.message_error = f'Error: reqId: {reqId}, errorCode: {errorCode}, message: {errorString}'
        self.message_error = "Error: " + str(reqId) + " " + str(errorCode) + " " + errorString
        print("Error: ", reqId, " ", errorCode, " ", errorString)

        if reqId != -1:
            self.flag_error_message = True
        # ловим ошибку 201 - послали контрактов больше чем может проглотить
        if errorCode == 201:
            self.flag_error_201 = True

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        #self.nextOrderId = orderId
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
        if key == 'NetLiquidation':
            self.flag_NetLiquidation_change = True
            self.NetLiquidation = f'{val} {currency}'

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
                  ", LastFillPrice: ", lastFillPrice)
            self.param_orderStatus = {'orderId': orderId, 'status': status, 'filled': filled, 'remaining': remaining,
                                      'lastFillPrice': lastFillPrice}
            # log_r.info("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ",
            # remaining, ", LastFillPrice: ", lastFillPrice)
            self.flag_orderStatus = True

        self.old_str_orderStatus = self.str_orderStatus

    def openOrder(self, orderId, contract, order, orderState):
        self.str_openOrder = f'OpenOrder. Id: {orderId}, {contract}, {order}, {orderState}'
        if self.old_str_openOrder != self.str_openOrder:
            print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":",
                  order.action, order.orderType, order.totalQuantity, orderState.status)
            self.param_openOrder = {'orderId': orderId, 'contract': contract, 'order': order, 'orderState': orderState}
            # log_r.info("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":",
            #            order.action, order.orderType, order.totalQuantity, orderState.status)
            self.flag_openOrder = True

        self.old_str_openOrder = self.str_openOrder

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)
        self.flag_execDetails = True  # сделка совершена на кол-во лотов  = execution.shares
        self.param_execDetails = {'contract': contract, 'execution': execution}
        # log_r.info("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
        #            execution.orderId, execution.shares, execution.lastLiquidity)

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
        self.contract_tz = contractDetails.timeZoneId
        self.flag_contractDetails = True

    def message_handler_terminal(self):
        try:
            try:
                text = self.msg_queue.get(block=True, timeout=0.2)
                if len(text) > MAX_MSG_LEN:
                    self.wrapper.error(NO_VALID_ID, BAD_LENGTH.code(),
                                       "%s:%d:%s" % (BAD_LENGTH.msg(), len(text), text))
                    return  # break
            except queue.Empty:
                logger.debug("queue.get: empty")
                self.msgLoopTmo()
            else:
                fields = comm.read_fields(text)
                logger.debug("fields %s", fields)
                self.decoder.interpret(fields)
                self.msgLoopRec()
        except (KeyboardInterrupt, SystemExit):
            logger.info("detected KeyboardInterrupt, SystemExit")
            self.keyboardInterrupt()
            self.keyboardInterruptHard()
        except BadMessage:
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
        self.mainwindow.lbl_Message_Edit.append(text)

    # читаем каледарь
    def ReadMOS(self):
        self.flag_read_mos = True
        try:
            with open("mos.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл mos.json отсутствует')
            log_r.critical('Файл mos.json отсутствует')
            # self.mainwindow.lbl_Message_Edit.append('Файл calendar.json отсутствует')
            self.MessageInfo('Файл mos.json отсутствует')
            # !!!!! вывод ошибки в окно сообщений робота
            return False

        print(f'mos: {loaded_json_file}')
        log_r.info(f'mos: {loaded_json_file}')

        self.mos = loaded_json_file["mos"]
        self.mos_list = list(self.mos.values())

        return True

    # читаем каледарь
    def ReadCalendar(self):
        self.flag_read_calendar = True
        try:
            with open("calendar.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл calendar.json отсутствует')
            log_r.critical('Файл calendar.json отсутствует')
            # self.mainwindow.lbl_Message_Edit.append('Файл calendar.json отсутствует')
            self.MessageInfo('Файл calendar.json отсутствует')
            # !!!!! вывод ошибки в окно сообщений робота
            return False

        print(f'config: {loaded_json_file}')
        log_r.info(f'config: {loaded_json_file}')

        self.tdw = loaded_json_file["Week"]
        self.tdm = loaded_json_file["Month"]
        return True

    # читаем конфиг
    def ReadConfig(self):

        self.flag_read_config = True
        try:
            with open("config.json", "r") as read_file:
                loaded_json_file = json.load(read_file)
        except FileNotFoundError:
            print(f'Файл config.json отсутствует')
            log_r.critical('Файл config.json отсутствует')
            self.MessageInfo('Файл config.json отсутствует')
            return False

        print(f'config: {loaded_json_file}')
        log_r.info(f'config: {loaded_json_file}')
        self.host = loaded_json_file["Host"]  # print(f'хост: {loaded_json_file["Host"]}') # по умолчанию 127.0.0.1
        # port - TWS demo 7497, IB Gateway demo 4002, TWS real 7496, IB Gateway real 4001
        self.port = int(
            loaded_json_file["Port"])  # print(f'port: {loaded_json_file["Port"]}') # по умолчанию 7497 - demo
        self.client_id = int(
            loaded_json_file["Client ID"])  # print(f'id: {loaded_json_file["Client ID"]}') # по умолчанию 1
        self.contract_1 = loaded_json_file["Contract"]  # print(f'id: {loaded_json_file["Contract"]}')  # по умолчанию 1
        self.time_to_act = loaded_json_file["Time_to_act"]

        self.mainwindow.lbl_host_Edit.setText(str(self.host))
        self.mainwindow.lbl_port_Edit.setText(str(self.port))
        self.mainwindow.lbl_client_id_Edit.setText(str(self.client_id))
        self.mainwindow.lbl_paper_Edit.setText(str(self.contract_1["localSymbol"]))

        return True

    def run(self):
        # self._mutex.lock()
        time_paper = datetime
        flag_flag_connect_old = False
        flag_correct_config = False
        flag_correct_calendar = False
        flag_correct_mos = False
        flag_time_paper = False
        contract_subtractor = 0
        cnt_request = 0  # счетчик медленных запросов
        CNT_REQ = 100  # запрашиваем 1 через 10 раз
        a = 0
        req = 1
        # try:
        print('123')

        # определяем объекты
        order = Order()
        contract = Contract()

        log_r.info('-------------- Новая Сессия ---------------')
        self.MessageInfo('-------------- Новая Сессия ---------------')

        # основной цикл робота
        # Читаем конфиг
        # Если конфига нет - выдаем ошибку и ничего не делаем

        while True:
            # проверка на нажатие кнопки Connect
            # если Была нажата Connect - соединяемся c сервером
            if self.mainwindow.flag_connect:

                # проверка на корректность конфига
                if (not flag_correct_config) or (not flag_correct_calendar) or \
                        (not flag_correct_mos):  # если конфиг, календарь или MOS не корректен - выходим
                    self.mainwindow.flag_connect = False
                    flag_flag_connect_old = False
                    self.mainwindow.btn_connect.setText('Connect')
                    continue

                log_r.info('Зашли во внешний цикл робота')
                flag_flag_connect_old = True

                # пытаемся соединиться с сервером
                self.connect(self.host, self.port, self.client_id)

                # конфигурируем наш контракт
                contract.symbol = self.contract_1['symbol']
                contract.secType = self.contract_1['secType']
                contract.exchange = self.contract_1['exchange']
                contract.currency = self.contract_1['currency']
                contract.localSymbol = self.contract_1['localSymbol']

                time.sleep(0.5)
                self.reqContractDetails(self.nextOrderId(), contract)
                time.sleep(0.1)
                self.reqMarketDataType(3)  # switch to delayed-frozen data if live is not available
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
                self.reqAccountUpdates(True, "")
                time.sleep(0.1)
                # сверяем полученный аккаунт c сервера и разрешенными аккаунтами в файле

                print("зашли в коннект")

                a = 0
                flag_account_true = False
                self.flag_position_change = True  # прочитаем позицию при входе в основной цикл
                flag_one_trade = False  # флаг одной попытки для сделки

                # try:
                while self.isConnected() or not self.msg_queue.empty():
                    # log_r.info('Зашли во внутренний цикл - цикл isConnect')
                    # self.mainwindow.lbl_Message_Edit.setText('Робот соединился с сервером')
                    self.mainwindow.lbl_server_conn_Edit.setText('YES')

                    # слушаем ответы от терминала
                    self.message_handler_terminal()

                    a = a + 1
                    print('a = ', a, ', tmp = ', self.mainwindow.tmp)
                    self.mainwindow.lbl1.setText(str(a))

                    if flag_account_true:  # если аккаунт валидный

                        # Основная программа тут

                        # Ждем время захода, если мы не в позиции
                        try:
                            if flag_time_paper: # if time_paper:  #контракт читали и время бумаги уже не None
                                # print("1:", time_paper.hour)
                                # мы не в позе
                                if not self.flag_Position:
                                    if time_paper.hour == int(self.time_to_act['input_hour']) \
                                            and time_paper.minute == int(self.time_to_act['input_min']) \
                                            and int(self.time_to_act['input_sec']) <= time_paper.second \
                                            and not flag_one_trade:  # сюда пока не заходили

                                        print("Время заходить")
                                        log_r.info("Время заходить")
                                        self.MessageInfo(f'Время заходить')
                                        flag_one_trade = True
                                        # читаем текущую котировку
                                        # Считаем - сегодня вообще заходим

                                        order_direction = "BUY"  # "SELL" #  берется из календаря - НАДО!!!
                                        number_of_lot = (0 - contract_subtractor) # кол-во лотов, рассчитывается от риска - НАДО!!!
                                        if number_of_lot <= 0:
                                            number_of_lot = 0
                                        log_r.info(f'Направление {order_direction}, кол-во контрактов {number_of_lot}')
                                        self.MessageInfo(f'Направление {order_direction}, кол-во контрактов {number_of_lot}')

                                        # насчитываем цену для входа
                                        if order_direction == "BUY":
                                            # если покупаем, берем цену на 10% выше текущей цены
                                            price_input = ((self.contract_price * 11) // 10)
                                        elif order_direction == "SELL":
                                            # если продаем, берем цену на 10% ниже текущей цены
                                            price_input = ((self.contract_price * 9) // 10)
                                        else:
                                            # если не торгуем
                                            price_input = 0

                                        # формируем ордер
                                        order.action = order_direction
                                        order.totalQuantity = number_of_lot
                                        order.orderType = "LMT"
                                        order.lmtPrice = price_input

                                        self.placeOrder(self.nextOrderId(), contract, order)
                                        # time.sleep(0.1)




                                # мы в позе
                                else:

                                    # ждем время выходить
                                    if time_paper.hour == self.time_to_act['output_hour'] and \
                                            time_paper.minute == self.time_to_act['output_min'] and \
                                            time_paper.second >= self.time_to_act['output_sec']:
                                        print("Время выходить")
                                        log_r.info("Время выходить")

                                        # допустим

                        except Exception:
                            print(f'Ошибка в flag_time_paper (?)')
                            log_r.info(f'Ошибка в flag_time_paper (?)')
                            self.MessageInfo(f'Ошибка в flag_time_paper (?)')

                        # //////////////////// МЕДЛЕННЫЕ ЗАПРОСЫ. Начало ////////////////////

                        # Запрашиваем 1 раз в 10 проходов
                        # cnt_request += 1
                        # if cnt_request >= CNT_REQ:
                        #     cnt_request = 0
                        #     # Запрос котировок
                        #     if not self.flag_tickPrice:
                        #         self.reqMktData(self.nextOrderId(), contract, "", False, False, [])
                        #     else:
                        #         self.flag_tickPrice = False
                        #         self.cancelMktData(self.nextOrderId())
                        #         self.mainwindow.lbl_paper_price_Edit.setText(str(self.contract_price))

                        # запрос времени с сервера (единичный, потокового нет)
                        # self.reqCurrentTime()  # -> def currentTime() -> server_time
                        # !!! сюда надо именно время сервера
                        local_time = datetime.now()
                        self.mainwindow.lbl_server_time_Edit.setText(str(local_time.strftime("%A, %d-%m-%Y, %H:%M:%S")))

                        # получаем время нашей бумаги
                        if self.contract_tz != "non":
                            time_paper = datetime.now(pytz.timezone(self.contract_tz))  # ('US/Central'))
                            flag_time_paper = True

                        self.mainwindow.lbl_working_time_Edit.setText(
                            str(time_paper.strftime("%A, %d-%m-%Y, %H:%M:%S")))

                        # если произошло изменелась цена контракта
                        if self.flag_contract_price_change:
                            self.flag_contract_price_change = False
                            self.mainwindow.lbl_paper_price_Edit.setText(str(self.contract_price))

                        # если произошло изменение в размере счета
                        if self.flag_NetLiquidation_change:
                            self.flag_NetLiquidation_change = False
                            self.mainwindow.lbl_account_size_Edit.setText(self.NetLiquidation)

                        # если произошло изменение в позиции
                        if self.flag_position_change:
                            self.flag_position_change = False
                            self.mainwindow.lbl_position_size_Edit.setText(str(self.position))

                            if self.position != 0:
                                self.mainwindow.lbl_robot_state_Edit.setText("In position")
                                self.flag_Position = True
                                flag_one_trade = False
                                # self.mainwindow.lbl_robot_state_Edit.setStyleSheet("color: green")
                            else:
                                self.mainwindow.lbl_robot_state_Edit.setText("Out of position")
                                self.flag_Position = False
                                # self.mainwindow.lbl_robot_state_Edit.setStyleSheet("color: red")

                        # если сделка совершена - либо отказы
                        if self.flag_execDetails:  # сделка совершена на кол-во лотов  = execution.shares
                            self.flag_execDetails = False
                            log_r.info(f'Trade: {self.param_execDetails["execution"].shares} contract(s), '
                                       f'Contract: {self.param_execDetails["contract"].localSymbol}')
                            self.MessageInfo(f'Trade: {self.param_execDetails["execution"].shares} contract(s), '
                                             f'Contract: {self.param_execDetails["contract"].localSymbol}')

                        if self.flag_orderStatus:
                            self.flag_orderStatus = False
                            log_r.info(f'OrderStatus: {self.param_orderStatus["status"]}, '
                                       f'Filled: {self.param_orderStatus["filled"]}, '
                                       f'Remaining: {self.param_orderStatus["remaining"]}, '
                                       f'LastFillPrice: {self.param_orderStatus["lastFillPrice"]}')
                            self.MessageInfo(f'OrderStatus: {self.param_orderStatus["status"]}, '
                                             f'Filled: {self.param_orderStatus["filled"]}, '
                                             f'Remaining: {self.param_orderStatus["remaining"]}, '
                                             f'LastFillPrice: {self.param_orderStatus["lastFillPrice"]}')

                            # если полностью закрыли сделку - пишем это
                            if self.param_orderStatus["status"] == "Filled" and self.param_orderStatus[
                                "remaining"] == 0:
                                log_r.info(f'Вход на {self.param_orderStatus["filled"]} контрактов завершён!')
                                self.MessageInfo(f'Вход на {self.param_orderStatus["filled"]} контрактов завершён!')
                                contract_subtractor = 0

                        # если заявку отклониили + ошибка: Поставили много контрактов

                        if self.flag_error_message:
                            self.flag_error_message = False
                            log_r.info(self.message_error)
                            self.MessageInfo(self.message_error)

                            if self.flag_error_201:
                                if self.param_orderStatus["status"] == "Inactive":
                                    self.flag_error_201 = False
                                    # то будем выставлять заново - уменьшив количество контрактов
                                    flag_one_trade = False
                                    contract_subtractor += 1

                        if self.flag_openOrder:
                            self.flag_openOrder = False
                            log_r.info(f'OpenOrder: {self.param_openOrder["order"].action}, '
                                       f'Status: {self.param_openOrder["orderState"].status}')
                            # self.MessageInfo(f'OpenOrder: {self.param_openOrder["order"].action}, '
                            #                  f'Status: {self.param_openOrder["orderState"].status}')
                            # print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange,
                            #       ":",
                            #       order.action, order.orderType, order.totalQuantity, orderState.status)
                            # self.param_openOrder = {'contract': contract, 'order': order, 'orderState': orderState}





                        # time_paper = (pytz.timezone('US/Central'))
                        # self.mainwindow.lbl_working_time_Edit.setText(str(time_paper.localize(datetime.now())))

                    # # time1 = datetime.fromtimestamp(time).strptime("%A, %B %d, %Y %H:%M:%S")
                    # # time2 = datetime.fromtimestamp(datetime.utcnow()).strptime("%A, %B %d, %Y %H:%M:%S")

                    # //////////////////// МЕДЛЕННЫЕ ЗАПРОСЫ. Конец ////////////////////

                    # Конец - if flag_account_true: # если аккаунт валидный

                    # проверка аккаунта на валидность
                    if self.flag_account_with_server and (not flag_account_true):
                        # если номер аккаунта прочитан с сервера - сверяем
                        try:
                            t = self.mos_list.index(self.account)
                            print(f'Аккаунт подтвержден: {self.account} is valid')
                            log_r.info(f'Аккаунт подтвержден: {self.account} is valid')
                            self.MessageInfo(f'Аккаунт подтвержден: {self.account} is valid')
                            self.mainwindow.lbl_account_Edit.setText(self.account)
                            flag_account_true = True
                            self.flag_account_with_server = False
                        except ValueError:
                            print(f'Неизвестный аккаунт: {self.account} is not valid')
                            log_r.info(f'Неизвестный аккаунт: {self.account} is not valid')
                            self.MessageInfo(f'Неизвестный аккаунт: {self.account} is not valid')
                            self.mainwindow.button_Connect()  # принудительно вызываем Кнопку Disconnect
                            self.cancelMktData(self.nextOrderId())
                            self.reqAccountUpdates(False, "")
                            self.flag_account_with_server = False

                    # нажали кнопку закрытия робота - будем рассоединяться
                    if self.mainwindow.close_app:
                        print('Закрыли Интерфейс')
                        log_r.info('Закрыли Интерфейс')
                        self.cancelMktData(self.nextOrderId())
                        self.reqAccountUpdates(False, "")

                        break

                    # если нажали Disconnect
                    if not self.mainwindow.flag_connect:
                        print('Нажали Disconnect')
                        log_r.info('Нажали Disconnect')
                        self.cancelMktData(self.nextOrderId())
                        self.reqAccountUpdates(False, "")
                        self.mainwindow.lbl_account_Edit.setText("-")
                        break

                # finally:
                print('Disconnect после закрытия окна')
                log_r.info('Нажали Disconnect')
                # self.disconnect()
                # self.connectionClosed()




            # иначе если нажали на Disconnect - разъединяемся с сервером
            elif not self.mainwindow.flag_connect and flag_flag_connect_old:
                print('Разъединение после Disconnect')
                log_r.info('Разъединение после Disconnect')
                # self.mainwindow.lbl_Message_Edit.setText(str('Связь с сервером прервана'))
                # self.connectionClosed()

                self.reqAccountUpdates(False, "")
                flag_flag_connect_old = False
                self.flag_read_config = False
                self.flag_read_calendar = False
                self.flag_read_mos = False
                self.disconnect()

                print('Разъединение после Disconnect 2')
                self.mainwindow.lbl_server_conn_Edit.setText('NO')
                time.sleep(1)


            # мы разъединены c сервером
            else:
                # self.MessageInfo(f'config: {self.mainwindow.flag_change_config1}')
                # print(f'config: {self.servicewindow.flag_change_config}')
                # пока не соединены с сервером читаем конфиг, либо перечитываем после изменения
                if (not self.flag_read_config) or self.servicewindow.flag_change_config:
                    flag_correct_config = self.ReadConfig()
                    self.servicewindow.flag_change_config = False

                #
                # if self.mainwindow.flag_change_config2 == 1:
                #     pass
                # else:
                #     flag_correct_config = self.ReadConfig()
                #     # self.mainwindow.flag_change_config = False  # сбрасываем флаг изменения конфига

                if not self.flag_read_calendar:
                    flag_correct_calendar = self.ReadCalendar()
                    # if not flag_correct_config:
                    # self.mainwindow.flag_connect = False
                    # flag_flag_connect_old = False
                    # self.mainwindow.btn_connect.setText('Connect')
                    # continue

                if not self.flag_read_mos:
                    flag_correct_mos = self.ReadMOS()

                a = a + 1
                print('a = ', a)
                print(self.mainwindow.flag_connect, ' ', flag_flag_connect_old)
                time.sleep(0.5)

                # self.mainwindow.lbl_server_time_Edit.setText(str(self.mainwindow.lbl_server_time_Edit.Text(),'- disconnect'))

        # finally:
        # except:
        #     raise
        # print('Вышли из основного robot.run.while')

        # self._mutex.unlock()

# def main():
#     # инициализация интерфейса
#     # win = Interface.QApplication(sys.argv)
#     # wU = win.Interface.WinUser()
#     # wS = Interface.WinService()
#     # sys.exit(win.exec_())
#     # win.exec_()
#
#     app = RobotApp()
#
#     app.connect("127.0.0.1", 7497, 1)
#
#     contract = Contract()
#     contract.symbol = "MES"
#     contract.secType = "FUT"
#     contract.exchange = "GLOBEX"
#     contract.currency = "USD"
#     contract.localSymbol = "MESU2"
#     # contract.primaryExchange = "NASDAQ"
#     time.sleep(1)
#     app.reqMarketDataType(3)  # switch to delayed-frozen data if live is not available
#     app.reqMktData(1, contract, "", False, False, [])
#     app.run()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     wU = WinUser()
#     wS = WinService()
#
#     rb = RobotApp(mainwindow=wU) # будем получать доступ к Окну
#     rb.connect("127.0.0.1", 7497, 1)
#
#     contract = Contract()
#     contract.symbol = "MES"
#     contract.secType = "FUT"
#     contract.exchange = "GLOBEX"
#     contract.currency = "USD"
#     contract.localSymbol = "MESU2"
#     # contract.primaryExchange = "NASDAQ"
#     time.sleep(1)
#     rb.reqMarketDataType(3)  # switch to delayed-frozen data if live is not available
#     rb.reqMktData(1, contract, "", False, False, [])
#     rb.start()
#     # def cnt():
#     #     a = 0
#     #     while 1:
#     #         a += 1
#     #         print(a)
#     #         time.sleep(1)
#     #
#     # threading.Thread(target=cnt, daemon=True).start()
#
#     sys.exit(app.exec_())
#     rb.join() # ожидание завершение потока rfr ,как будто бы не нужен - до него дело не доходит
#
