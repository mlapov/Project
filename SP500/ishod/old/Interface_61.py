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
import json
import robot
import robot_telebot
import logging

# from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QFrame, QGridLayout, QComboBox, QTextBrowser)

from PyQt5.QtCore import QCoreApplication, Qt, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib  # Email
# import telebot  # telegram
from threading import Thread


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
    logging.basicConfig(filename=time.strftime("log/system.%d-%m-%Y.log"),  # ("log/system.%d-%m-%Y_%H%M%S.log"),
                        filemode="a",
                        encoding='utf-8',
                        level=logging.ERROR,
                        format=recfmt, datefmt=timefmt)

    # logger = logging.getLogger()
    # console = logging.StreamHandler()
    # console.setLevel(logging.ERROR)
    # logger.addHandler(console)


def buffer(flag):
    buf_flag = flag
    return buf_flag


# класс отправки почты
class SendEmail(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.i = 0
        self.flag_sent_email = False
        self.flag_run_email = True
        self.host_email = ""
        self.subject_email = ""
        self.to_addr_email = ""
        self.from_addr_email = ""
        self.password_email = ""
        self.body_text_email = ""

    def send_email(self, host, subject, to_addr, from_addr, password, body_text):
        """
        Send an email
        """
        # BODY = "\r\n".join((
        #     "From: %s" % from_addr,
        #     "To: %s" % to_addr,
        #     "Subject: %s" % subject,
        #     "",
        #     body_text
        # ))
        msg = MIMEMultipart()  # MIME нужен для русских букв - без него на русские буквы ругается
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        server = smtplib.SMTP(host)
        server.starttls()
        server.login(msg['From'], password)
        try:
            # server.sendmail(from_addr, to_addr, BODY)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f"Successfully sent email from {from_addr} to {to_addr}: {body_text}")
        except:
            print("Сообщение на email послать не удалось!")
            print(f"Successfully sent email from {from_addr} to {to_addr}:\n{body_text}")

        server.quit()

    def run(self):
        while self.flag_run_email:
            print(f"from Email: {self.i}")
            self.i += 1
            time.sleep(0.5)
            if self.flag_sent_email:
                self.flag_sent_email = False

                self.send_email(self.host_email,
                                self.subject_email,
                                self.to_addr_email,
                                self.from_addr_email,
                                self.password_email,
                                self.body_text_email)


# class Interface(QWidget):
class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initWin()  # инициализация окна
        # -self.initWinService()  # инициализация окна

    #     Пользовательское окно
    def initWin(self):
        self.resize(460, 700)
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

        # Индикация - Размер счета полный = бумаги + деньги
        self.lbl_account_size = QLabel('Account Size: ', self)
        self.lbl_account_size_Edit = QLabel('-', self)

        # Индикация - Кол-во свободных средств
        self.lbl_available_funds = QLabel('Available funds: ', self)
        self.lbl_available_funds_Edit = QLabel('-', self)

        # индикация - Код бумаги
        self.lbl_paper = QLabel('Contract: ', self)
        self.lbl_paper_Edit = QLabel('-', self)

        # индикация - Рабочее время
        self.lbl_working_time = QLabel('Contract trading time: ', self)
        self.lbl_working_time_Edit = QLabel('-', self)

        # индикация - Текущая цена контракт
        self.lbl_paper_price = QLabel('Price: ', self)
        self.lbl_paper_price_Edit = QLabel('-', self)

        # риск на сделку
        self.lbl_risk = QLabel('Risk per trade: ', self)
        self.lbl_risk_Edit = QLabel('-', self)

        # оценочный минимальный депоизт
        self.lbl_min_depo = QLabel('Min Account Size (estimated): ', self)
        self.lbl_min_depo_Edit = QLabel('-', self)

        # состояние робота
        self.lbl_robot_state = QLabel('Robot state: ', self)
        self.lbl_robot_state_Edit = QLabel('-', self)
        # self.lbl_robot_state_Edit.setStyleSheet("QLabel {color:green}")
        # Направление сделки - Buy, Sell
        self.lbl_direction = QLabel('Direction: ', self)
        self.lbl_direction_Edit = QLabel('-', self)

        # индикация размера позиции по бумаги
        self.lbl_position_size = QLabel('Position size: ', self)
        self.lbl_position_size_Edit = QLabel('0', self)

        # точка входа
        self.lbl_price_input_trade = QLabel('Price input: ', self)
        self.lbl_price_input_trade_Edit = QLabel('0', self)

        # стоп
        self.lbl_price_stop_trade = QLabel('Price stop: ', self)
        self.lbl_price_stop_trade_Edit = QLabel('0', self)

        self.lbl_empty = QLabel('', self)

        # Сообщения в основном окне
        self.lbl_Message = QLabel('Messages: ', self)
        self.lbl_Message_Edit = QTextBrowser(self)  # №QTextEdit(self)
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
        grid.addWidget(self.lbl_available_funds, N_str, 0)
        grid.addWidget(self.lbl_available_funds_Edit, N_str, 1)

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
        grid.addWidget(self.lbl_risk, N_str, 0)
        grid.addWidget(self.lbl_risk_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_min_depo, N_str, 0)
        grid.addWidget(self.lbl_min_depo_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_robot_state, N_str, 0)
        grid.addWidget(self.lbl_robot_state_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_direction, N_str, 0)
        grid.addWidget(self.lbl_direction_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_position_size, N_str, 0)
        grid.addWidget(self.lbl_position_size_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_price_input_trade, N_str, 0)
        grid.addWidget(self.lbl_price_input_trade_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_price_stop_trade, N_str, 0)
        grid.addWidget(self.lbl_price_stop_trade_Edit, N_str, 1)

        N_str += 1
        grid.addWidget(self.lbl_empty, N_str, 0)

        N_str += 1
        grid.addWidget(self.lbl_Message, N_str, 0)
        N_str += 1
        grid.addWidget(self.lbl_Message_Edit, N_str, 0, (N_str + 3), 2)

        # Организаця Ввода/Вывода из строки
        # self.lbl1 = QLabel('Zetcode', self)
        # # self.lbl1.move(25, 20)
        # self.title1_Edit = QLineEdit(self)
        # # self.title1_Edit.move(95, 20)

        # btnBtn = QPushButton('Кнопка', self)
        # btnBtn.setToolTip('Соединение с кнопкой')
        # # btnBtn.resize(btnBtn.sizeHint())
        # # btnBtn.move(200, 20)
        # btnBtn.clicked.connect(self.buttonBtn)

        # # Галочки!!!
        # self.cb = QCheckBox('Цель НЕ установлена', self)
        # # self.cb.move(300, 20)
        # # self.cb.toggle()
        # self.cb.stateChanged.connect(self.changeTarget)
        # # self.lbl2 = QLabel('Цель НЕ установлена', self)
        # # self.lbl2.move(320, 20)

        # field_other = QHBoxLayout()
        # field_other.addWidget(self.lbl1)
        # field_other.addWidget(self.title1_Edit)
        # field_other.addWidget(btnBtn)
        # field_other.addWidget(self.cb)

        # Вызываем Сервис через кнопку
        btn = QPushButton('Сервис', self)
        btn.setToolTip('Вызов окна Сервис')
        # btn.resize(btn.sizeHint())
        # btn.move(100, 200)
        btn.clicked.connect(self.buttonService)
        field_other2 = QVBoxLayout()
        field_other2.addLayout(grid)
        # field_other2.addLayout(field_other)
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
        print("Послали коннект")
        print(f"флаг1 flag_connect {self.flag_connect}")

    # Обработка кнопки Сервис
    def buttonService(self):
        wS.show()

    def MessageInfo(self, text):
        self.lbl_Message_Edit.append(text)
        # try:
        #     WinUser.show()
        # except: print(Exception)

    def FromConfig(self, fromconfig):
        self.lbl_host_Edit.setText(fromconfig["lbl_host_Edit"])
        self.lbl_port_Edit.setText(fromconfig["lbl_port_Edit"])
        self.lbl_client_id_Edit.setText(fromconfig["lbl_client_id_Edit"])
        self.lbl_paper_Edit.setText(fromconfig["lbl_paper_Edit"])
        self.lbl_risk_Edit.setText(fromconfig["lbl_risk_Edit"])

    # это сигналы из RobotApp для отображения
    def FromRobotApp(self, fromrobotapp):
        # self.btn_connect.setText(fromrobotapp["btn_connect"])
        self.lbl_server_conn_Edit.setText(fromrobotapp["lbl_server_conn_Edit"])
        self.lbl_server_time_Edit.setText(fromrobotapp["lbl_server_time_Edit"])
        self.lbl_account_Edit.setText(fromrobotapp["lbl_account_Edit"])
        self.lbl_account_size_Edit.setText(fromrobotapp["lbl_account_size_Edit"])
        self.lbl_available_funds_Edit.setText(fromrobotapp["lbl_available_funds_Edit"])
        self.lbl_working_time_Edit.setText(fromrobotapp["lbl_working_time_Edit"])
        self.lbl_paper_price_Edit.setText(fromrobotapp["lbl_paper_price_Edit"])
        self.lbl_min_depo_Edit.setText(fromrobotapp["lbl_min_depo_Edit"])
        self.lbl_robot_state_Edit.setText(fromrobotapp["lbl_robot_state_Edit"])
        self.lbl_direction_Edit.setText(fromrobotapp["lbl_direction_Edit"])
        self.lbl_position_size_Edit.setText(fromrobotapp["lbl_position_size_Edit"])
        self.lbl_price_input_trade_Edit.setText(fromrobotapp["lbl_price_input_trade_Edit"])
        self.lbl_price_stop_trade_Edit.setText(fromrobotapp["lbl_price_stop_trade_Edit"])

    # Обработка кнопки Соединение
    # def buttonBtn(self):
    #     # print(f'config: {self.flag_change_config1}')
    #     text = self.title1_Edit.text()
    #     QMessageBox.about(self, "Сообщение", text)
    #     self.tmp = int(text)

    # self.QMessageBox.setText(text)
    # self.QMessageBox.exec();

    # # Установка цели
    # def changeTarget(self, state):
    #     if state == Qt.Checked:
    #         self.cb.setText('Цель Установлена')
    #     else:
    #         self.cb.setText('Цель НЕ установлена')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close_app = True
            self.flag_connect = False
            wS.closeWinService()
            event.accept()
        else:
            event.ignore()


# Окно сервиса
class WinService(Interface):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(QtCore.Qt.Window)
        self.logging_level = "ERROR"  # значение по умолчанию
        self.flag_logging_level = True
        self.flag_reset = False
        self.btn_reset = None
        self.resize(460, 500)
        self.btn_save = None
        self.centralWidget = None
        self.initWinService()
        self.flag_change_config = False

    def initWinService(self):

        self.setWindowTitle("Service")
        self.move((300 + 460), 300)  # X, Y где 0 это сверху-слева, 460 - ширина Основного окна

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

        lbl_empty = QLabel('', self)

        # Редактирование Connect. Начало
        lbl_host = QLabel('Host', self)
        self.lbl_host_Edit = QLineEdit(self)
        self.lbl_host_Edit.setText(loaded_json_file["Host"])
        # self.lbl_host_btn = QPushButton('Change', self)

        lbl_port = QLabel('Port', self)
        self.lbl_port_Edit = QLineEdit(self)
        self.lbl_port_Edit.setText(loaded_json_file["Port"])

        # lbl_crib1 = QLabel('- Live Trading ports: TWS: 7496; IB Gateway: 4001', self)
        # lbl_crib2 = QLabel('- Simulated Trading ports: TWS 7497; IB Gateway: 4002', self)
        # # self.lbl_port_btn = QPushButton('Change', self)

        lbl_client_id = QLabel('Client ID', self)
        self.lbl_client_id_Edit = QLineEdit(self)
        self.lbl_client_id_Edit.setText(loaded_json_file["Client ID"])
        # self.lbl_client_id_btn = QPushButton('Change', self)

        lbl_contract = QLabel('Contract', self)
        self.lbl_contract_Edit = QLineEdit(self)
        self.lbl_contract_Edit.setText(loaded_json_file["Contract"]["localSymbol"])
        # self.lbl_contract_btn = QPushButton('Change', self)

        lbl_risk = QLabel('Risk, %', self)
        self.lbl_risk_Edit = QLineEdit(self)
        self.lbl_risk_Edit.setText(str(loaded_json_file["risk"]))

        lbl_email = QLabel('Email', self)
        self.lbl_email_Edit = QLineEdit(self)
        self.lbl_email_Edit.setText(loaded_json_file["Email"])

        lbl_telegram = QLabel('Telegram Token', self)
        self.lbl_telegram_Edit = QLineEdit(self)
        self.lbl_telegram_Edit.setText(loaded_json_file["Telegram_token"])

        self.btn_save = QPushButton('Save', self)
        # self.btn_save.maximumSize()
        self.btn_save.setToolTip('Сохранить изменения')
        self.btn_save.clicked.connect(self.button_Save)  # Сохраняем

        self.btn_reset = QPushButton('Robot Reset', self)
        self.btn_reset.size()
        self.btn_reset.setToolTip('Сброс робота')
        self.btn_reset.clicked.connect(self.button_Reset)  # Сброс робота

        self.lbl_log = QLabel('Logging level', self)
        self.lbl_log_Edit = QComboBox(self)
        self.lbl_log_Edit.addItems(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"])
        self.lbl_log_Edit.activated[str].connect(self.loggingLevel)
        self.lbl_log_Edit.setCurrentIndex(0 if self.logging_level == "CRITICAL" else \
                                              1 if self.logging_level == "ERROR" else \
                                                  2 if self.logging_level == "WARNING" else \
                                                      3 if self.logging_level == "INFO" else \
                                                          4 if self.logging_level == "DEBUG" else 0)  # значение по умолчанию

        self.lbl_work_session = QLabel('Working session', self)
        self.lbl_work_session_Edit = QLabel('-', self)

        self.lbl_direction = QLabel('Direction', self)
        self.lbl_direction_Edit = QLabel('-', self)

        self.lbl_week_day = QLabel('Weekday', self)
        self.lbl_week_day_Edit = QLabel('-', self)

        self.lbl_days_in_trend = QLabel('Days in trend', self)
        self.lbl_days_in_trend_Edit = QLabel('-', self)

        self.lbl_trend_delta = QLabel('Trend delta', self)
        self.lbl_trend_delta_Edit = QLabel('-', self)

        self.lbl_order_direction = QLabel('PreOrder', self)
        self.lbl_order_direction_Edit = QLabel('-', self)

        self.lbl_available_funds = QLabel('Available funds: ', self)
        self.lbl_available_funds_Edit = QLabel('-', self)

        self.lbl_go = QLabel('CurrInitMargin', self)
        self.lbl_go_Edit = QLabel('-', self)

        self.lbl_svv = QLabel('SVV', self)
        self.lbl_svv_Edit = QLabel('-', self)

        self.lbl_relative_stop = QLabel('Relative Stop (Current)', self)
        self.lbl_relative_stop_Edit = QLabel('-', self)

        self.lbl_absolute_stop = QLabel('Absolute Stop', self)
        self.lbl_absolute_stop_Edit = QLabel('-', self)

        self.lbl_loss_1_lot = QLabel('Loss per lot', self)
        self.lbl_loss_1_lot_Edit = QLabel('-', self)

        self.lbl_abs_loss_1_trade = QLabel('Risk on deposit', self)
        self.lbl_abs_loss_1_trade_Edit = QLabel('-', self)

        self.lbl_number_of_lot = QLabel('Entry to N lots', self)
        self.lbl_number_of_lot_Edit = QLabel('-', self)

        grid = QGridLayout()
        grid.setSpacing(1)
        N_str = 1
        grid.addWidget(lbl_host, N_str, 0)
        grid.addWidget(self.lbl_host_Edit, N_str, 1)
        # grid.addWidget(self.lbl_host_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_port, N_str, 0)
        grid.addWidget(self.lbl_port_Edit, N_str, 1)
        # N_str += 1
        # grid.addWidget(lbl_crib1, N_str, 1)
        # N_str += 1
        # grid.addWidget(lbl_crib2, N_str, 1)
        # N_str += 1
        # grid.addWidget(lbl_empty, N_str, 1)
        # grid.addWidget(self.lbl_port_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_client_id, N_str, 0)
        grid.addWidget(self.lbl_client_id_Edit, N_str, 1)
        # grid.addWidget(self.lbl_client_id_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_contract, N_str, 0)
        grid.addWidget(self.lbl_contract_Edit, N_str, 1)
        # grid.addWidget(self.lbl_contract_btn, N_str, 2)
        N_str += 1
        grid.addWidget(lbl_risk, N_str, 0)
        grid.addWidget(self.lbl_risk_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(lbl_email, N_str, 0)
        grid.addWidget(self.lbl_email_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(lbl_telegram, N_str, 0)
        grid.addWidget(self.lbl_telegram_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.btn_save, N_str, 1)
        N_str += 1
        grid.addWidget(self.btn_reset, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_log, N_str, 0)
        grid.addWidget(self.lbl_log_Edit, N_str, 1)
        N_str += 2
        grid.addWidget(self.lbl_work_session, N_str, 0)
        grid.addWidget(self.lbl_work_session_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_direction, N_str, 0)
        grid.addWidget(self.lbl_direction_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_week_day, N_str, 0)
        grid.addWidget(self.lbl_week_day_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_days_in_trend, N_str, 0)
        grid.addWidget(self.lbl_days_in_trend_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_trend_delta, N_str, 0)
        grid.addWidget(self.lbl_trend_delta_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_order_direction, N_str, 0)
        grid.addWidget(self.lbl_order_direction_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_available_funds, N_str, 0)
        grid.addWidget(self.lbl_available_funds_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_go, N_str, 0)
        grid.addWidget(self.lbl_go_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_svv, N_str, 0)
        grid.addWidget(self.lbl_svv_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_relative_stop, N_str, 0)
        grid.addWidget(self.lbl_relative_stop_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_absolute_stop, N_str, 0)
        grid.addWidget(self.lbl_absolute_stop_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_loss_1_lot, N_str, 0)
        grid.addWidget(self.lbl_loss_1_lot_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_abs_loss_1_trade, N_str, 0)
        grid.addWidget(self.lbl_abs_loss_1_trade_Edit, N_str, 1)
        N_str += 1
        grid.addWidget(self.lbl_number_of_lot, N_str, 0)
        grid.addWidget(self.lbl_number_of_lot_Edit, N_str, 1)

        main_layout = QVBoxLayout(self.centralWidget)
        main_layout.addLayout(grid)
        # main_layout.addLayout(field_other)
        # main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

    # кнопка сброса робота
    def button_Reset(self, event):

        if wU.flag_connect:  # если связь с сервером есть - то можно сбросить робота
            reply = QMessageBox.question(self, 'Message',
                                         "Вы хотите сбросить робота?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.flag_reset = True
            else:
                pass  # event.ignore()
        else:  # если связи с сервером нет
            QMessageBox.question(self, 'Message',
                                 "Сброс робота возможен \nтолько после соединения с Сервером",
                                 QMessageBox.Ok)

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
            risk = self.lbl_risk_Edit.text()
            email = self.lbl_email_Edit.text()
            telegram_token = self.lbl_telegram_Edit.text()

            # читаем файл конфига
            with open("config.json", "r") as read_file:
                loaded_json_file = json.load(read_file)

            # перезаписываем данные
            loaded_json_file["Host"] = host
            loaded_json_file["Port"] = port
            loaded_json_file["Client ID"] = client_id
            loaded_json_file["Contract"]["localSymbol"] = contract
            # loaded_json_file["risk"] = risk
            loaded_json_file["Email"] = email
            loaded_json_file["Telegram_token"] = telegram_token
            try:
                if type(int(risk)) is int:
                    if int(risk) >= 0 and int(risk) <= 100:  #
                        loaded_json_file["risk"] = risk
                    else:
                        print(f"Risk (!) не в диапазоне (0-100): {risk}")
                        logging.critical(f"Risk (!) не в диапазоне (0-100): {risk}")
                        wU.lbl_Message_Edit.append(f"Risk не в диапазоне (0-100): {risk}")
            except:
                print(f"Недопустимое значение Risk`a: {risk}")
                logging.critical(f"Недопустимое значение Risk`a: {risk}")
                wU.lbl_Message_Edit.append(f"Недопустимое значение Risk`a: {risk}")

            # записываем в конфиг обратно
            # Запись в файл:
            with open("config.json", "w") as write_file:
                json.dump(loaded_json_file, write_file, indent=4)

            self.flag_change_config = True  # ставим флаг изменения конфига - чтобы перечитать

            # self.close_app = True
            # event.accept()
        else:
            pass  # event.ignore()

    def loggingLevel(self, text):
        self.flag_logging_level = True  # ставим флаг изменения ровня логирования
        self.logging_level = text

        if self.logging_level == "DEBUG":
            logging.getLogger().setLevel(logging.DEBUG)
        elif self.logging_level == "INFO":
            logging.getLogger().setLevel(logging.INFO)
        elif self.logging_level == "WARNING":
            logging.getLogger().setLevel(logging.WARNING)
        elif self.logging_level == "ERROR":
            logging.getLogger().setLevel(logging.ERROR)
        elif self.logging_level == "CRITICAL":
            logging.getLogger().setLevel(logging.CRITICAL)
        else:
            pass

    def closeWinService(self):
        self.close()

    # это сигналы из RobotApp для отображения в окне Сервис
    def FromRobotApp(self, fromrobotapp):
        self.lbl_work_session_Edit.setText(fromrobotapp["lbl_work_session_Edit"])
        self.lbl_direction_Edit.setText(fromrobotapp["lbl_direction_Edit"])
        self.lbl_week_day_Edit.setText(fromrobotapp["lbl_week_day_Edit"])
        self.lbl_days_in_trend_Edit.setText(fromrobotapp["lbl_days_in_trend_Edit"])
        self.lbl_trend_delta_Edit.setText(fromrobotapp["lbl_trend_delta_Edit"])
        self.lbl_order_direction_Edit.setText(fromrobotapp["lbl_order_direction_Edit"])
        self.lbl_available_funds_Edit.setText(fromrobotapp["lbl_available_funds_Edit"])
        self.lbl_go_Edit.setText(fromrobotapp["lbl_go_Edit"])
        self.lbl_svv_Edit.setText(fromrobotapp["lbl_svv_Edit"])
        self.lbl_relative_stop_Edit.setText(fromrobotapp["lbl_relative_stop_Edit"])
        self.lbl_absolute_stop_Edit.setText(fromrobotapp["lbl_absolute_stop_Edit"])
        self.lbl_loss_1_lot_Edit.setText(fromrobotapp["lbl_loss_1_lot_Edit"])
        self.lbl_abs_loss_1_trade_Edit.setText(fromrobotapp["lbl_abs_loss_1_trade_Edit"])
        self.lbl_number_of_lot_Edit.setText(fromrobotapp["lbl_number_of_lot_Edit"])
        # if fromrobotapp["flag_change_config"] == "False":
        #     self.flag_change_config = False
        # if fromrobotapp["flag_reset"] == "False":
        #     self.flag_reset = False
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

# logr = logging.getLogger(__name__)

# if not os.path.exists("log"):
#     os.makedirs("log")
# log_i = logging.getLogger('interface')
# log_i.setLevel(logging.INFO)
# fi = logging.FileHandler()  #("log/interface.log", 'a', 'utf-8')  # каждый раз новый файл 'w', дозапись 'a'
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fi.setFormatter(formatter)
# log_i.addHandler(fi)

if __name__ == '__main__':
    # Будем вести лог = lag_log = True, не будем вести лог - False
    # flag_log = False
    # flag_log = True
    # if flag_log:
    SetupLogger()
    logging.critical("Запустили интерфейс")  # log_i.info("Запустили интерфейс")

    app = QApplication(sys.argv)
    wU = WinUser()
    wS = WinService()
    sE = SendEmail()
    # tB1 = robot_telebot.TelegramBot("non_interactive")
    # tB2 = robot_telebot.TelegramBot("interactive")
    # rb = robot.RobotApp(mainwindow=wU, servicewindow=wS, email=sE, telegram=tB1,
    #                     telegram_interactive=tB2)  # будем получать доступ к Окну

    rb = robot.RobotApp(mainwindow=wU, servicewindow=wS, email=sE)  # будем получать доступ к Окну

    # сигналы из Алгоритма в Основное окно
    rb.MessageInfoToQT.connect(wU.MessageInfo, Qt.QueuedConnection)
    rb.FromConfigToQT.connect(wU.FromConfig, Qt.QueuedConnection)
    rb.FromRobotAppToQT.connect(wU.FromRobotApp, Qt.QueuedConnection)
    # rb.ButtonConnectToQT.connect(wU.button_Connect, Qt.QueuedConnection)

    # сигналы из Алгоритма в окно Сервис
    rb.FromRobotAppToQT_srv.connect(wS.FromRobotApp, Qt.QueuedConnection)

    rb.start()  # запускаем поток основного цикла
    sE.start()
    # tB1.start()
    # tB2.start()

    sys.exit(app.exec_())
