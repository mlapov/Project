
"""
Чисто интерфейс

"""

import sys
import threading
import time

from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QApplication, QMainWindow, QAction, qApp, QTextEdit, QCheckBox)

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

# class Interface(QWidget):
class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initWin()           # инициализация окна
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
        self.initWinUser()

    def initWinUser(self):
        self.setWindowTitle("Robot")

        # Вызываем Сервис через кнопку
        btn = QPushButton('Сервис', self)
        btn.setToolTip('Вызов окна Сервис')
        btn.resize(btn.sizeHint())
        btn.move(100, 200)
        btn.clicked.connect(self.buttonService)

        # Организация Меню
        serviceAction = QAction(QIcon('exit.png'), '&сервис', self)
        serviceAction.setStatusTip('Открыть окно Сервис')
        serviceAction.triggered.connect(self.buttonService) #(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Меню')
        fileMenu.addAction(serviceAction)
        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Menubar')

        # Организаця Ввода/Вывода из строки
        lbl1 = QLabel('Zetcode', self)
        lbl1.move(25, 20)
        self.title1_Edit = QLineEdit(self)
        self.title1_Edit.move(95,20)
        btnConnect = QPushButton('Соединение', self)
        btnConnect.setToolTip('Соединение с Сервером')
        btnConnect.resize(btn.sizeHint())
        btnConnect.move(200, 20)
        btnConnect.clicked.connect(self.buttonConnect)


        # Галочки!!!
        self.cb = QCheckBox('Цель НЕ установлена', self)
        self.cb.move(300, 20)
        # self.cb.toggle()
        self.cb.stateChanged.connect(self.changeTarget)
        # self.lbl2 = QLabel('Цель НЕ установлена', self)
        # self.lbl2.move(320, 20)

        # Отображаем окно
        self.show()

    # Обработка кнопки Сервис
    def buttonService(self):
        wS.show()
        # try:
        #     WinUser.show()
        # except: print(Exception)



    # Обработка кнопки Соединение
    def buttonConnect(self):
        text = self.title1_Edit.text()

        QMessageBox.about(self, "Сообщение", text)
        # self.QMessageBox.setText(text)
        # self.QMessageBox.exec();

    # Установка цели
    def changeTarget(self,state):
        if state == Qt.Checked:
            self.cb.setText('Цель Установлена')
        else:
            self.cb.setText('Цель НЕ установлена')




    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
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
        self.move(400,400)
        # self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)

    wU = WinUser()
    wS = WinService()

    def cnt():
        a = 0
        while 1:
            a += 1
            print(a)
            time.sleep(1)

    threading.Thread(target=cnt, daemon=True).start()

    sys.exit(app.exec_())
