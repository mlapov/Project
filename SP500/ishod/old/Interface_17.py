"""
работает подсоединение с сервером
коннект и доисконнект корректны
Пара =  файл robot_5 + Interface_5

"""
import datetime
import os
import sys
from threading import Thread
import time

import robot
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame, QGridLayout)

from PyQt5.QtCore import QCoreApplication, Qt, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


def SetupLogger():
    # создаем папку с логами если ее нет
    if not os.path.exists("log"):
        os.makedirs("log")
    # создаем новый файл каждый раз
    # time.strftime("system.%d%m%Y_%H%M%S.log")
    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'
    timefmt = '%d-%m-%Y_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    # конфигурируем отображение
    # DEBUG 	Детальная информация, интересная только при отладке
    #
    # INFO 	    Подтверждение, что все работает как надо
    #
    # WARNING 	Индикация того, что что-то пошло не так, и возможны проблемы в будущем
    #           (заканчивается место на диске, етс)
    #           Программа продолжает работать как надо.
    #
    # ERROR 	Относительно серьезная проблема, программа не смогла выполнить некоторый функционал.
    #
    # CRITICAL 	Реально серьезная проблема, программа не может работать дальше.
    logging.basicConfig(filename=time.strftime("log/system.%d-%m-%Y_%H%M%S.log"),
                        filemode="w",
                        encoding='utf-8',
                        level=logging.DEBUG,
                        format=recfmt, datefmt=timefmt)

    # logger = logging.getLogger()
    # console = logging.StreamHandler()
    # console.setLevel(logging.ERROR)
    # logger.addHandler(console)


def buffer(flag):
    buf_flag = flag
    return buf_flag


# class Interface(QWidget):
class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initWin()  # инициализация окна
        # -self.initWinService()  # инициализация окна

    #     Пользовательское окно
    def initWin(self):
        self.resize(450, 650)
        self.move(300, 300)  # координаты на Рабочем столе
        self.setWindowTitle("None")
        # self.show()


# Окно Пользователя
class WinUser(Interface):
    def __init__(self):
        super().__init__()
        self.lbl_Message = None
        self.lbl_Message_Edit = None
        self.serviceAction = None
        self.btn_connect = None
        self.frame = None
        self.lbl1 = None
        self.title1_Edit = None
        self.centralWidget = None
        self.lbl_client_id_Edit = None
        self.lbl_port_Edit = None
        self.lbl_host_Edit = None
        self.initWinUser()
        self.tmp = 0
        self.close_app = False  # флаг закрытия Интерфейса, True - закрыт
        self.flag_connect = False  # True - нажата кнопка Connect, False - состояние Disconnect

    def initWinUser(self):
        self.setWindowTitle("Robot")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Инициализируем Connect. Начало
        lbl_host = QLabel('Host', self)
        self.lbl_host_Edit = QLineEdit(self)
        self.lbl_host_Edit.setReadOnly(True)  # поле только на чтение
        lbl_port = QLabel('Port', self)
        self.lbl_port_Edit = QLineEdit(self)
        self.lbl_port_Edit.setReadOnly(True)  # поле только на чтение
        lbl_client_id = QLabel('Client ID', self)
        self.lbl_client_id_Edit = QLineEdit(self)
        self.lbl_client_id_Edit.setReadOnly(True)  # поле только на чтение
        self.btn_connect = QPushButton('Connect', self)
        self.btn_connect.setToolTip('Соединение с сервером')
        self.btn_connect.clicked.connect(self.button_Connect)  # запускаем Коннект

        field_connect = QHBoxLayout()

        field_connect.addWidget(lbl_host)
        field_connect.addWidget(self.lbl_host_Edit)
        field_connect.addWidget(lbl_port)
        field_connect.addWidget(self.lbl_port_Edit)
        field_connect.addWidget(lbl_client_id)
        field_connect.addWidget(self.lbl_client_id_Edit)
        field_connect.addWidget(self.btn_connect)
        # Инициализируем Connect. Конец

        # Индикация - Связь с сервером
        self.lbl_server_conn = QLabel('Server connection: ', self)
        self.lbl_server_conn_Edit = QLabel('NO', self)

        # Индикация - Время сервера
        self.lbl_server_time = QLabel('Server Time: ', self)
        self.lbl_server_time_Edit = QLabel('xx:xx:xx ', self)
        # field_server = QHBoxLayout()
        # field_server.addWidget(self.lbl_server_time)
        # field_server.addWidget(self.lbl_server_time_Edit)

        # Индикация - Номер счета
        self.lbl_account = QLabel('Account: ', self)
        self.lbl_account_Edit = QLabel('-', self)

        # Индикация - Номер счета
        self.lbl_account_size = QLabel('Account Size: ', self)
        self.lbl_account_size_Edit = QLabel('-', self)

        # индикация - Код бумаги
        self.lbl_paper = QLabel('Contract: ', self)
        self.lbl_paper_Edit = QLabel('-', self)

        # индикация - Рабочее время
        self.lbl_working_time = QLabel('Contract trading time: ', self)
        self.lbl_working_time_Edit = QLabel('NO', self)

        # индикация - Текущая цена контракт
        self.lbl_paper_price = QLabel('Price: ', self)
        self.lbl_paper_price_Edit = QLabel('-', self)

        # состояние робота
        self.lbl_robot_state = QLabel('Robot state: ', self)
        self.lbl_robot_state_Edit = QLabel('-', self)

        # индикация размера позиции по бумаги
        self.lbl_position_size = QLabel('Position size: ', self)
        self.lbl_position_size_Edit = QLabel('0', self)

        self.lbl_empty = QLabel('', self)

        # Сообщения в основном окне
        self.lbl_Message = QLabel('Messages: ', self)
        self.lbl_Message_Edit = QTextEdit(self)
        # self.lbl_Message_Edit.setText()
        self.lbl_Message_Edit.setReadOnly(True)  # поле только на чтение
        # размещаем Параметры по таблице

        grid = QGridLayout()
        grid.setSpacing(1)
        N_str = 1
        grid.addWidget(self.lbl_server_conn, N_str, 0)
        grid.addWidget(self.lbl_server_conn_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_server_time, N_str, 0)
        grid.addWidget(self.lbl_server_time_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_account, N_str, 0)
        grid.addWidget(self.lbl_account_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_account_size, N_str, 0)
        grid.addWidget(self.lbl_account_size_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_paper, N_str, 0)
        grid.addWidget(self.lbl_paper_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_working_time, N_str, 0)
        grid.addWidget(self.lbl_working_time_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_paper_price, N_str, 0)
        grid.addWidget(self.lbl_paper_price_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_robot_state, N_str, 0)
        grid.addWidget(self.lbl_robot_state_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_position_size, N_str, 0)
        grid.addWidget(self.lbl_position_size_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_empty, N_str, 0)

        N_str += 1
        grid.addWidget(self.lbl_Message, N_str, 0)
        N_str += 1
        grid.addWidget(self.lbl_Message_Edit, N_str, 0, (N_str + 3), 2)

        # Организаця Ввода/Вывода из строки
        self.lbl1 = QLabel('Zetcode', self)
        # self.lbl1.move(25, 20)
        self.title1_Edit = QLineEdit(self)
        # self.title1_Edit.move(95, 20)

        btnBtn = QPushButton('Кнопка', self)
        btnBtn.setToolTip('Соединение с кнопкой')
        # btnBtn.resize(btnBtn.sizeHint())
        # btnBtn.move(200, 20)
        btnBtn.clicked.connect(self.buttonBtn)

        # Галочки!!!
        self.cb = QCheckBox('Цель НЕ установлена', self)
        # self.cb.move(300, 20)
        # self.cb.toggle()
        self.cb.stateChanged.connect(self.changeTarget)
        # self.lbl2 = QLabel('Цель НЕ установлена', self)
        # self.lbl2.move(320, 20)

        field_other = QHBoxLayout()
        field_other.addWidget(self.lbl1)
        field_other.addWidget(self.title1_Edit)
        field_other.addWidget(btnBtn)
        field_other.addWidget(self.cb)

        # Вызываем Сервис через кнопку
        btn = QPushButton('Сервис', self)
        btn.setToolTip('Вызов окна Сервис')
        # btn.resize(btn.sizeHint())
        # btn.move(100, 200)
        btn.clicked.connect(self.buttonService)
        field_other2 = QVBoxLayout()
        field_other2.addLayout(grid)
        field_other2.addLayout(field_other)
        field_other2.addWidget(btn)

        # Организуем виджеты в окне

        self.frame = QFrame()
        self.frame.setMinimumSize(200, 200)
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setLayout(field_other2)

        main_layout = QVBoxLayout(self.centralWidget)
        main_layout.addLayout(field_connect)
        # main_layout.addLayout(field_other)
        main_layout.addWidget(self.frame)

        self.setLayout(main_layout)

        # Организация Меню и статус бара
        self.serviceAction = QAction(QIcon('exit.png'), '&сервис', self)
        self.serviceAction.setStatusTip('Открыть окно Сервис')
        self.serviceAction.triggered.connect(self.buttonService)  # (qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Меню')
        fileMenu.addAction(self.serviceAction)
        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Menubar')

        # Отображаем окно
        self.show()

    # Обработка кнопки Connect
    def button_Connect(self):
        # если мы нажали на Disconnect -  flag_connect был в True -> перключаем на Disconnect
        if self.flag_connect:
            self.flag_connect = False
            self.btn_connect.setText('Connect')
            # !!!!! надо на статус баре выводить что "Status: Disconnected..."
            # rb.disconnect()
        # если мы нажали на Connect -  flag_connect был в False -> перключаем на Connect
        else:
            self.flag_connect = True
            self.btn_connect.setText('Disconnect')
            # !!!!! надо на статус баре выводить что "Status: Connect!"

    # Обработка кнопки Сервис
    def buttonService(self):
        wS.show()

        # try:
        #     WinUser.show()
        # except: print(Exception)

    # Обработка кнопки Соединение
    def buttonBtn(self):
        # print(f'config: {self.flag_change_config1}')
        text = self.title1_Edit.text()
        QMessageBox.about(self, "Сообщение", text)
        self.tmp = int(text)

        # self.QMessageBox.setText(text)
        # self.QMessageBox.exec();

    # Установка цели
    def changeTarget(self, state):
        if state == Qt.Checked:
            self.cb.setText('Цель Установлена')
        else:
            self.cb.setText('Цель НЕ установлена')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close_app = True
            event.accept()
        else:
            event.ignore()


import json


# Окно сервиса
class WinService(Interface):
    def __init__(self):
        super().__init__()
        self.resize(450, 350)
        self.btn_save = None
        self.centralWidget = None
        self.initWinService()
        self.flag_change_config = False

    def initWinService(self):

        self.setWindowTitle("Service")
        self.move(400, 400)

        # self.show()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        try:
            with open("config.json", "r") as read_file:
                loaded_json_file = json.load(read_file)

        except FileNotFoundError:
            print(f'Файл config.json отсутствует')
            # log_r.critical('Файл config.json отсутствует')
            # self.MessageInfo('Файл config.json отсутствует')
            lbl_no_config = QLabel('Файл config.json отсутствует', self)
            lbl_no_config.setAlignment(Qt.AlignCenter)
            main_layout = QVBoxLayout(self.centralWidget)
            main_layout.addWidget(lbl_no_config)
            # main_layout.addLayout(field_other)
            # main_layout.addWidget(self.frame)
            self.setLayout(main_layout)
            return

        # Редактирование Connect. Начало
        lbl_host = QLabel('Host', self)
        self.lbl_host_Edit = QLineEdit(self)
        self.lbl_host_Edit.setText(loaded_json_file["Host"])
        self.lbl_host_btn = QPushButton('Change', self)

        lbl_port = QLabel('Port', self)
        self.lbl_port_Edit = QLineEdit(self)
        self.lbl_port_Edit.setText(loaded_json_file["Port"])
        self.lbl_port_btn = QPushButton('Change', self)

        lbl_client_id = QLabel('Client ID', self)
        self.lbl_client_id_Edit = QLineEdit(self)
        self.lbl_client_id_Edit.setText(loaded_json_file["Client ID"])
        self.lbl_client_id_btn = QPushButton('Change', self)

        lbl_contract = QLabel('Contract', self)
        self.lbl_contract_Edit = QLineEdit(self)
        self.lbl_contract_Edit.setText(loaded_json_file["Contract"]["localSymbol"])
        self.lbl_contract_btn = QPushButton('Change', self)

        self.btn_save = QPushButton('Save', self)
        self.btn_save.setToolTip('Сохранить изменения')
        self.btn_save.clicked.connect(self.button_Save)  # Сохраняем

        grid = QGridLayout()
        grid.setSpacing(1)
        N_str = 1
        grid.addWidget(lbl_host, N_str, 0)
        grid.addWidget(self.lbl_host_Edit, N_str, 1)
        grid.addWidget(self.lbl_host_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_port, N_str, 0)
        grid.addWidget(self.lbl_port_Edit, N_str, 1)
        grid.addWidget(self.lbl_port_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_client_id, N_str, 0)
        grid.addWidget(self.lbl_client_id_Edit, N_str, 1)
        grid.addWidget(self.lbl_client_id_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_contract, N_str, 0)
        grid.addWidget(self.lbl_contract_Edit, N_str, 1)
        grid.addWidget(self.lbl_contract_btn, N_str, 2)
        N_str += 1
        grid.addWidget(self.btn_save, N_str, 0)

        main_layout = QVBoxLayout(self.centralWidget)
        main_layout.addLayout(grid)
        # main_layout.addLayout(field_other)
        # main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

    # сохраняем изменения из окна Сервиса
    def button_Save(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Сохранить изменения?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:

            # читаем данные из окна
            host = self.lbl_host_Edit.text()
            port = self.lbl_port_Edit.text()
            client_id = self.lbl_client_id_Edit.text()
            contract = self.lbl_contract_Edit.text()

            # читаем файл конфига
            with open("config.json", "r") as read_file:
                loaded_json_file = json.load(read_file)

            # перезаписываем данные
            loaded_json_file["Host"] = host
            loaded_json_file["Port"] = port
            loaded_json_file["Client ID"] = client_id
            loaded_json_file["Contract"]["localSymbol"] = contract

            # записываем в конфиг обратно
            # Запись в файл:
            with open("config.json", "w") as write_file:
                json.dump(loaded_json_file, write_file)

            self.flag_change_config = True  # ставим флаг изменения конфига - чтобы перечитать

            # self.close_app = True
            # event.accept()
        else:
            pass  # event.ignore()

    #
    #
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Вы точно хотите выйти?\n\nPS: В случае внесения изменений \nнеобходимо переконнектиться!",
    #                                  QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         self.close_app = True
    #         event.accept()
    #     else:
    #         event.ignore()


import logging

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
import robot

# logr = logging.getLogger(__name__)

if not os.path.exists("log"):
    os.makedirs("log")
log_i = logging.getLogger('interface')
log_i.setLevel(logging.INFO)
fh = logging.FileHandler("log/interface.log", 'a', 'utf-8')  # каждый раз новый файл 'w', дозапись 'a'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log_i.addHandler(fh)

if __name__ == '__main__':

    # Будем вести лог = lag_log = True, не будем вести лог - False
    flag_log = False
    # flag_log = True
    if flag_log:
        SetupLogger()
    log_i.info("Запустили интерфейс")

    app = QApplication(sys.argv)
    wU = WinUser()
    wS = WinService()

    rb = robot.RobotApp(mainwindow=wU, servicewindow=wS)  # будем получать доступ к Окну
    rb.start()  # запускаем поток основного цикла

    sys.exit(app.exec_())
