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

    - Стопы надо ставить GTC

    - хранить не номера счетов, а их ХЕШи

    - если запустьить Коннект - потом открыть Сервис - потом закрыть Основное окно - то Сервис висит а
    а потом закрывается с ошибкой в терминале - т.е. при закрытии Основного окна, надо также чистить
    и закрвать Сервис

    - если запустить робота без TWS - робота выкидывает с ошибкой при нажатии на Коннект,
    надо чтобы робота не выкидывало, а писал, чтонет TWSа

    - если вдруг TWS ерезагружается - робот вылетает с ошибкой - надо чтобы робот висел - пытался соединять,
    но не вылетал

    - уведомления через емейл, телеграм - https://github.com/liiight/notifiers
    (см в телеграм канале Senior Python Developer)

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
from ibapi.utils import (current_fn_name, BadMessage, intMaxString, decimalMaxString, floatMaxString)
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


class RobotApp(QThread, EWrapper, EClient):
    def __init__(self, mainwindow, servicewindow, *args, **kwargs):
        EClient.__init__(self, self)
        super(RobotApp, self).__init__(*args, **kwargs)

        self.flag_5_min_candle = False
        self.price_stop_trade = 0
        self.price_input_trade = 0
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
        self.NUM_DAY_CANDLE = 45  # количество считываемых свечек
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
            print(orderState.status, orderState.initMarginBefore, orderState.maintMarginBefore,
                  orderState.equityWithLoanBefore, "1:", orderState.initMarginChange, orderState.maintMarginChange,
                  orderState.equityWithLoanChange, orderState.initMarginAfter, orderState.maintMarginAfter,
                  orderState.equityWithLoanAfter, orderState.commission, orderState.minCommission,
                  orderState.maxCommission, orderState.commissionCurrency, orderState.warningText,
                  orderState.completedTime, orderState.completedStatus)
            if (float(orderState.initMarginChange) > 0) \
                    and (float(orderState.initMarginChange) < 1000000):   # защита - проскакивают очень большие числа - если большое число - просто не учитываем
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
            else:
                print("historicalDataEnd. Массив свечек не корректен", self.index_day_candle, "!=",
                      self.NUM_DAY_CANDLE)
                self.flag_day_candle = False

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

    # округление до тика в большую сторону ("+") или в меньшую ("-")

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
        self.risk = loaded_json_file["risk"]

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
        self.delta_trend = loaded_json_file["delta"]
        self.svv_day = loaded_json_file["svv"]
        self.stop_percent = loaded_json_file["stop_percent"]
        self.price_input_trade = loaded_json_file["price_input"]
        self.price_stop_trade = loaded_json_file["price_stop"]

        self.mainwindow.lbl_host_Edit.setText(str(self.host))
        self.mainwindow.lbl_port_Edit.setText(str(self.port))
        self.mainwindow.lbl_client_id_Edit.setText(str(self.client_id))
        self.mainwindow.lbl_paper_Edit.setText(str(self.contract_1["localSymbol"]))

        return True

    def R_W_config(self, param="", val=None):
        # читаем файл конфига
        with open("config.json", "r") as read_file:
            loaded_json_file = json.load(read_file)
        # перезаписываем данные
        loaded_json_file[param] = val
        # записываем в конфиг обратно
        # Запись в файл:
        with open("config.json", "w") as write_file:
            json.dump(loaded_json_file, write_file)

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
                log_r.info(f'Trade: Направление для сделки (BUY,SELL) не задано')
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
                log_r.info(f'Trade: Хотим совершить сделку на 0 контрактов!')
                self.MessageInfo(f'Trade: Хотим совершить сделку на 0 контрактов!')
                return
        else:
            print('Trade: Направление для сделки (INPUT,OUTPUT) не определено')
            log_r.info(f'Trade: Направление для сделки (INPUT,OUTPUT) не определено')
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
        cnt_reqHistoricalData = 0  # счетчик для чтения свечек
        cnt_request = 0  # счетчик медленных запросов
        CNT_REQ = 100  # запрашиваем 1 через 10 раз
        num_month = ""
        work_session = 0
        week_day = 0
        # DELTA_TREND = 2  # порог дельта в тренде
        dict_week_day = {0: "Monday ", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday",
                         6: "Sunsday"}
        order_direction = "None"
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
                self.reqAccountUpdates(True, "")
                time.sleep(0.1)
                # self.reqHistoricalData(self.nextOrderId(), contract, "", "10 D", "1 day", "TRADES", 0, 1, False, [])
                # time.sleep(0.1)

                # сверяем полученный аккаунт c сервера и разрешенными аккаунтами в файле
                print("зашли в коннект")
                # self.reqAllOpenOrders()
                a = 0
                flag_account_true = False
                self.flag_position_change = True  # прочитаем позицию при входе в основной цикл
                flag_one_trade = False  # флаг одной попытки для сделки
                cnt_reqHistoricalData = 0
                # try:
                while self.isConnected() or not self.msg_queue.empty():
                    # log_r.info('Зашли во внутренний цикл - цикл isConnect')
                    # self.mainwindow.lbl_Message_Edit.setText('Робот соединился с сервером')
                    self.mainwindow.lbl_server_conn_Edit.setText('YES')

                    # слушаем ответы от терминала
                    self.message_handler_terminal()

                    a = a + 1
                    print('a = ', a)  # , ', tmp = ', self.mainwindow.tmp)
                    # self.mainwindow.lbl1.setText(str(a))
                    if flag_account_true:  # если аккаунт валидный

                        # Основная программа тут

                        # Ждем время захода, если мы не в позиции
                        try:
                            if flag_time_paper:  # if time_paper:  #контракт читали и время бумаги уже не None

                                # мы не в позе
                                if not self.flag_Position:
                                    if time_paper.hour == int(self.time_to_act['input_hour']) \
                                            and time_paper.minute == int(self.time_to_act['input_min']) \
                                            and int(self.time_to_act['input_sec']) <= time_paper.second \
                                            and order_direction != "None" \
                                            and not flag_one_trade:  # сюда пока не заходили

                                        print("Время заходить")
                                        log_r.info("Время заходить")
                                        self.MessageInfo(f'Время заходить')
                                        flag_one_trade = True
                                        # читаем текущую котировку
                                        # Считаем - сегодня вообще заходим

                                        # !!!!! для Debug. Начало
                                        # order_direction = "BUY"  # закомментировать для обычной работы
                                        # !!!!! для Debug. Конец

                                        number_of_lot -= contract_subtractor  # кол-во лотов, рассчитывается от риска - НАДО!!!
                                        if number_of_lot <= 0:
                                            number_of_lot = 0
                                        log_r.info(f'Направление {order_direction}, кол-во контрактов {number_of_lot}')
                                        self.MessageInfo(
                                            f'Направление {order_direction}, кол-во контрактов {number_of_lot}')

                                        # рассчитываем стоп
                                        # absolute_stop = 4000

                                        self.Trade(contract=contract, trd="INPUT", order_direction=order_direction,
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

                                # мы в позе
                                else:
                                    print('1:', flag_one_trade)
                                    # ждем время выхода
                                    if time_paper.hour == int(self.time_to_act['output_hour']) \
                                            and time_paper.minute == int(self.time_to_act['output_min']) \
                                            and int(self.time_to_act['output_sec']) <= time_paper.second \
                                            and not flag_one_trade:  # сюда пока не заходили

                                        print("Время выходить")
                                        log_r.info("Время выходить")
                                        self.MessageInfo(f'Время выходить')
                                        flag_one_trade = True

                                        # Принятие решения - выходим или оставляем на следующий день
                                        flag_need_output = True  # !!!!! надо сбрасывать после обнуления позиции

                                        # если нужно выходить
                                        if flag_need_output:
                                            self.Trade(contract=contract, trd="OUTPUT", position=self.position,
                                                       contract_price=self.contract_price, orderType="LMT")
                                            self.R_W_config(param="price_input", val=0)
                                            flag_output = True


                                        else:
                                            print("Переносим позицию на следующий день")
                                            log_r.info("Переносим позицию на следующий день")
                                            self.MessageInfo(f'Переносим позицию на следующий день')
                            # else:
                            #     print("b")


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

                        # анализируем 5-ти минутки
                        if self.flag_5_min_candle:
                            self.flag_5_min_candle = False

                            if self.index_day_candle == 2:
                                cnt_reqHistoricalData = 0
                                self.flag_read_5mins = True
                            elif self.index_day_candle == 3:
                                # Предолагаем что последнняя свеча - это наша искомая
                                self.price_input_trade = float(self.day_candle[self.index_day_candle - 1]['o'])
                                self.R_W_config(param="price_input", val=self.price_input_trade)
                                print("Ориентировочная точка входа:", self.price_input_trade)

                        # если массив дневных свечек заполнены - считаем сессию и тренд
                        if self.flag_day_candle:
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
                            self.servicewindow.lbl_work_session_Edit.setText(str(work_session))
                            # определяем направление захода
                            direction = self.tdm[str(work_session)]
                            if direction == "+L":  # если сегодня в лонг
                                direction = "BUY"  # будем покупать
                            elif direction == "-L":  # если сегодня в шорт
                                direction = "SELL"  # будем продавать
                            else:
                                direction = "NONE"  # иначе ничего
                            print("Направление по календарю", direction)
                            self.servicewindow.lbl_direction_Edit.setText('/') if direction == "BUY" else \
                                self.servicewindow.lbl_direction_Edit.setText('None')

                            # определяем текущий день недели
                            week_day = time_paper.weekday()
                            print("День недели", dict_week_day[week_day])
                            self.servicewindow.lbl_week_day_Edit.setText(dict_week_day[week_day])

                            # определяем тренд
                            trend = self.tdw[str(week_day)]
                            if trend > 23:  # проверка на дурака - в месяце не бывает более 23 рабочих дней
                                pass  # раскомментировать  для работы trend = 23
                            delta = self.day_candle[self.NUM_DAY_CANDLE - 1]['c'] - \
                                    self.day_candle[self.NUM_DAY_CANDLE - 1 - trend]['c']
                            print("Дней в тренде", trend, ", дельта тренда", delta)
                            self.servicewindow.lbl_days_in_trend_Edit.setText(str(trend))
                            self.servicewindow.lbl_trend_delta_Edit.setText(str(delta) + ' /') if delta >= 0 else \
                                self.servicewindow.lbl_trend_delta_Edit.setText(str(delta) + ' \\')

                            # определим приказ
                            if direction == "BUY" and trend > 0 and delta >= self.delta_trend:
                                order_direction = direction
                            elif direction == "SELL" and trend > 0 and delta <= -self.delta_trend:
                                order_direction = direction
                            else:
                                order_direction = "None"
                            print("ПреПриказ", order_direction)
                            self.servicewindow.lbl_order_direction_Edit.setText(str(order_direction))

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

                            self.servicewindow.lbl_svv_Edit.setText(str(round(svv, 2)))
                            # self.servicewindow.lbl_relative_stop_Edit.setText(str(relative_stop))
                            # !!!!! стересть дебаг
                            # order_direction = "BUY"
                            # абсолютный стоп = открытие дня +- относительный стоп
                            if order_direction == "BUY":  # если покупаем - стоп будем ставить ниже
                                absolute_stop = (self.day_candle[self.NUM_DAY_CANDLE]['o'] - relative_stop)
                            elif order_direction == "SELL":  # если продаем - стоп будем ставить выше
                                absolute_stop = (self.day_candle[self.NUM_DAY_CANDLE]['o'] + relative_stop)
                            else:
                                absolute_stop = 0
                            print(f'Абсолютный стоп = {absolute_stop}')
                            self.servicewindow.lbl_absolute_stop_Edit.setText(str(absolute_stop))

                            # Проверка - а не ушла ли цена за пределы стопа? - заходить не будем если так
                            if order_direction == "BUY":
                                # если нам в лонг и текущая цена ниже стопа (чуть ухудшаем текущую цену)
                                if absolute_stop >= (self.contract_price - (4 * self.minTick)):
                                    order_direction = "None"
                                    print("Цена возле стопа или ниже: стоп =", absolute_stop, ", цена = ",
                                          (self.contract_price - (4 * self.minTick)), ", сброс приказа в",
                                          order_direction)

                            if order_direction == "SELL":
                                # если нам в шорт и текущая цена выше стопа (чуть ухудшаем текущую цену)
                                if absolute_stop <= (self.contract_price + (4 * self.minTick)):
                                    order_direction = "None"
                                    print("Цена возле стопа или выше: стоп =", absolute_stop, ", цена = ",
                                          (self.contract_price - (4 * self.minTick)), ", сброс приказа в",
                                          order_direction)

                            # Вычисляем на сколько будем заходить в зависимости от риска
                            # считаем сколько потеряем в баксах одним лотом
                            if order_direction != "None" and absolute_stop > 0:
                                loss_1_lot = abs(absolute_stop - self.contract_price) * self.pip_price
                            else:
                                loss_1_lot = 0
                            relative_stop_curr = (abs(absolute_stop - self.contract_price)) if absolute_stop != 0 else 0
                            print(f'Относительный стоп текущий = {relative_stop_curr}')
                            print(
                                f'Потеря на один лот = {loss_1_lot}')  # (({absolute_stop}-{self.contract_price})*{self.pip_price})')
                            self.servicewindow.lbl_relative_stop_Edit.setText(str(relative_stop) + ' (' +
                                                                              str(relative_stop_curr) + ')')
                            self.servicewindow.lbl_loss_1_lot_Edit.setText(f'{loss_1_lot} {self.currency_account}')

                            # считаем - сколько готовы потерять исходя из риска и нашего депозита
                            abs_loss_1_trade = (self.free_money * self.risk) / 100
                            print(f'При риске {self.risk}% из {self.free_money} готовы потерять {abs_loss_1_trade}')
                            self.servicewindow.lbl_abs_loss_1_trade_Edit.setText(f'{round(abs_loss_1_trade, 2)} '
                                                                                 f'{self.currency_account} '
                                                                                 f'({self.risk}%)')

                            # Т.о. размер входа в лотах составляет
                            number_of_lot = int(abs_loss_1_trade // loss_1_lot) if loss_1_lot != 0 else 0
                            print(f'Будем заходить на {number_of_lot} лотов')
                            self.servicewindow.lbl_number_of_lot_Edit.setText(str(number_of_lot))

                            # рассчитаем минимальный депозит
                            min_depo = ((
                                                    loss_1_lot * 100) / self.risk) * 1.02 if self.risk != 0 else 0  # немного увеличиваем минимальный депозит
                            print(f'Оценочный минимальный депозит равен {round(min_depo, 2)}')
                            self.mainwindow.lbl_min_depo_Edit.setText(f'{min_depo} {self.currency_account}')

                        # если изменилась цена контракта
                        if self.flag_contract_price_change:
                            self.flag_contract_price_change = False
                            self.mainwindow.lbl_paper_price_Edit.setText(str(self.contract_price))

                            # запросим данные по свечам (будем заказывать с периодом 10)
                            if cnt_reqHistoricalData == 0:
                                cnt_reqHistoricalData = 10
                                if self.flag_read_5mins:  # если надо прочитать пятиминутки
                                    self.reqHistoricalData(self.nextOrderId(), contract, "",
                                                           "40 S", "5 mins", "TRADES", 0, 1, False, [])
                                else:    # иначе читаем дни
                                    self.reqHistoricalData(self.nextOrderId(), contract, "",
                                                           str(self.NUM_DAY_CANDLE) + " D",
                                                           "1 day", "TRADES", 0, 1, False, [])

                                self.index_day_candle = 1
                                self.Trade(contract=contract, trd="INPUT",
                                           order_direction=order_direction if order_direction != "None" else "BUY",
                                           position=1, contract_price=self.contract_price,
                                           orderType="LMT", real="demo")

                            cnt_reqHistoricalData -= 1

                        # если произошло изменение в размере счета
                        if self.flag_NetLiquidation_change:
                            self.flag_NetLiquidation_change = False
                            self.mainwindow.lbl_account_size_Edit.setText(self.NetLiquidation)
                            self.mainwindow.lbl_available_funds_Edit.setText(self.AvailableFunds)
                            self.servicewindow.lbl_available_funds_Edit.setText(self.AvailableFunds)

                        # если произошло изменение в позиции
                        if self.flag_position_change:
                            self.flag_position_change = False
                            self.mainwindow.lbl_position_size_Edit.setText(str(self.position))

                            if self.position != 0:
                                self.mainwindow.lbl_robot_state_Edit.setText("In position")
                                self.flag_Position = True
                                # flag_one_trade = False
                                # self.mainwindow.lbl_robot_state_Edit.setStyleSheet("color: green")
                            else:
                                self.mainwindow.lbl_robot_state_Edit.setText("Out of position")
                                self.flag_Position = False
                                flag_need_output = False
                                # flag_one_trade = False
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
                            # self.MessageInfo(f'OrderStatus: {self.param_orderStatus["status"]}, '
                            #                  f'Filled: {self.param_orderStatus["filled"]}, '
                            #                  f'Remaining: {self.param_orderStatus["remaining"]}, '
                            #                  f'LastFillPrice: {self.param_orderStatus["lastFillPrice"]}')

                            # если полностью закрыли сделку - пишем это
                            if self.param_orderStatus["status"] == "Filled" and self.param_orderStatus[
                                "remaining"] == 0:
                                log_r.info(f'Сделка на {self.param_orderStatus["filled"]} контракт(ов) завершёна!')
                                self.MessageInfo(f'Сделка на {self.param_orderStatus["filled"]} контракт(ов) завершён!')
                                contract_subtractor = 0

                                # если полностью закрыли сделку после входа в позу - формируем стоп
                                if flag_input:
                                    self.flag_Position = True
                                    flag_one_trade = False
                                    flag_input = False
                                    # формируем стоп
                                    if order_direction == "BUY":
                                        order_direction = "SELL"
                                    elif order_direction == "SELL":
                                        order_direction = "BUY"

                                    order.action = order_direction
                                    order.totalQuantity = self.param_orderStatus["filled"]
                                    order.orderType = "STP"
                                    order.auxPrice = absolute_stop
                                    # self.simplePlaceOid = self.nextOrderId()
                                    self.placeOrder(self.nextOrderId(), contract, order)
                                    # print("self.simplePlaceOid = ", self.simplePlaceOid)
                                    self.R_W_config(param="price_stop", val=absolute_stop)
                                    # запрос параметров текущей свечи - для определения ориентировочной точки входа
                                    # для этого обнулим счетчик чтений свечек - чтобы читал по принуждению
                                    cnt_reqHistoricalData = 0
                                    self.flag_read_5mins = True

                                # если полностью закрыли сделку после выхода из позы - убираем все заявки
                                if flag_output:
                                    self.flag_Position = False
                                    flag_one_trade = False
                                    # flag_output = False
                                    # self.reqGlobalCancel() # снимаем все ордера
                                    # self.cancelOrder(self.simplePlaceOid, "") # снимаем конкретный ордер
                                    self.reqOpenOrders()


                        if self.flag_openOrderEnd:
                            self.flag_openOrderEnd = False

                            # закрываем стопы после выхода из позы
                            if flag_output:
                                flag_output = False
                                if (self.param_openOrder["order"].clientId == self.client_id) and \
                                        (self.param_openOrder["order"].orderType == "STP" or \
                                         self.param_openOrder["order"].orderType == "STP LTM"):
                                    self.cancelOrder(self.param_openOrder["orderId"], "")
                                    self.R_W_config(param="price_stop", val=0)
                                    self.R_W_config(param="price_input", val=0)


                        # если заявку отклонили + ошибка: Поставили много контрактов

                        if self.flag_error_message:
                            self.flag_error_message = False
                            log_r.info(self.message_error)
                            # self.MessageInfo(self.message_error)

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
                            self.servicewindow.lbl_go_Edit.setText(f'{round(self.go, 2)} {self.currency_account}')
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
                            self.mainwindow.lbl_risk_Edit.setText(str(self.risk) + "%")
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

                    # Сброс робота
                    if self.servicewindow.flag_reset:
                        # закрываем позы если есть
                        if self.flag_Position:
                            self.Trade(contract=contract, trd="OUTPUT", position=self.position,
                                       contract_price=self.contract_price, orderType="LMT")
                        # закрываем стопы если есть
                        flag_output = True
                        self.R_W_config(param="price_input", val=0)
                        self.R_W_config(param="price_stop", val=0)
                        self.mainwindow.button_Connect()

                        break

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

                if self.servicewindow.flag_reset:
                    self.servicewindow.flag_reset = False
                    print(f'Произведен сброс робота')
                    log_r.info(f'Произведен сброс робота')
                    self.MessageInfo(f'Произведен сброс робота')
                    self.mainwindow.button_Connect()
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
