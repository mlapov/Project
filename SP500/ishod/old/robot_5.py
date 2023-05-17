"""
работает подсоединение с сервером
коннект и доисконнект корректны
Пара =  файл robot_5 + Interface_5

"""

import sys
from threading import Thread
import time

from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame)

from PyQt5.QtCore import QCoreApplication, Qt, QThread, QMutex
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


import logging
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

logger = logging.getLogger(__name__)

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
import time


class RobotApp(QThread, EWrapper, EClient):
    def __init__(self, mainwindow, *args, **kwargs):
        EClient.__init__(self, self)
        super(RobotApp, self).__init__(*args, **kwargs)
        self.nextOrderId = 1
        self.mainwindow = mainwindow  # получаем доступ к окну
        self._mutex = QMutex()

        # QThread.daemon = True  # выключает поток при закрытии интерфейса
    # def connectionClosed(self):
    #     print('46')
    #     EClient.disconnect()

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        print("MarketDataType. ReqId:", reqId, "Type:", marketDataType)

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

    def run(self):
        # self._mutex.lock()
        flag_flag_connect_old = False
        a = 0
        req = 1
        # try:
        print('123')
        # основной цикл робота
        while True:
            # проверка на нажатие кнопки Connect
            # если Была нажата Connect - соединяемся c сервером
            if self.mainwindow.flag_connect:
                flag_flag_connect_old = True
                self.connect("127.0.0.1", 7497, 1)

                contract = Contract()
                contract.symbol = "MES"
                contract.secType = "FUT"
                contract.exchange = "GLOBEX"
                contract.currency = "USD"
                contract.localSymbol = "MESU2"
                # contract.primaryExchange = "NASDAQ"
                time.sleep(1)

                self.reqMarketDataType(3)  # switch to delayed-frozen data if live is not available
                self.reqMktData(self.nextOrderId, contract, "", False, False, [])
                print("зашли в коннект")

                a = 0
                # try:
                while self.isConnected() or not self.msg_queue.empty():
                    self.message_handler_terminal()
                    a = a + 1
                    print('a = ', a, ', tmp = ', self.mainwindow.tmp)
                    self.mainwindow.lbl1.setText(str(a))

                    # нажали кнопку закрытия робота - будем рассоединяться
                    if self.mainwindow.close_app:
                        print('Закрыли Интерфейс')
                        self.cancelMktData(self.nextOrderId)
                        # req +=1
                        # self.disconnect()
                        # self.connectionClosed()
                        break

                    # если нажали Disconnect
                    if not self.mainwindow.flag_connect:
                        print('Нажали Disconnect')
                        self.cancelMktData(self.nextOrderId)
                        # req += 1
                        # self.disconnect()
                        # self.connectionClosed()

                        break


                # finally:
                print('Disconnect после закрытия окна')
                # self.disconnect()
                # self.connectionClosed()




            # иначе если нажали на Disconnect - разъединяемся с сервером
            elif not self.mainwindow.flag_connect and flag_flag_connect_old:
                print('Разъединение после Disconnect')
                # self.connectionClosed()
                flag_flag_connect_old = False

                self.disconnect()
                print('Разъединение после Disconnect 2')
                time.sleep(1)


            # мы разъединены c сервером
            else:
                a = a + 1
                print('a = ', a)
                print(self.mainwindow.flag_connect, ' ', flag_flag_connect_old)
                time.sleep(0.5)


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
