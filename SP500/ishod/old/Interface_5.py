"""
работает подсоединение с сервером
коннект и доисконнект корректны
Пара =  файл robot_5 + Interface_5

"""

import sys
from threading import Thread
import time

import robot
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame)

from PyQt5.QtCore import QCoreApplication, Qt, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


# class Interface(QWidget):
class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initWin()  # инициализация окна
        # -self.initWinService()  # инициализация окна

    #     Пользовательское окно
    def initWin(self):
        self.resize(450, 250)
        self.move(300, 300)  # координаты на Рабочем столе
        self.setWindowTitle("None")
        # self.show()


# Окно Пользователя
class WinUser(Interface):
    def __init__(self):
        super().__init__()
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
        lbl_port = QLabel('Port', self)
        self.lbl_port_Edit = QLineEdit(self)
        lbl_client_id = QLabel('Client ID', self)
        self.lbl_client_id_Edit = QLineEdit(self)
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


# Окно сервиса
class WinService(Interface):
    def __init__(self):
        super().__init__()
        self.initWinService()

    def initWinService(self):
        self.setWindowTitle("Service")
        self.move(400, 400)
        # self.show()


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

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wU = WinUser()
    wS = WinService()

    rb = robot.RobotApp(mainwindow=wU)  # будем получать доступ к Окну
    rb.start()


    sys.exit(app.exec_())
