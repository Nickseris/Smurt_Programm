#импорт библиотек и модулей
from pygame import *
from random import randint
from time import time as timer
mixer.init()
font.init()
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from shooter_game.py import TOTAL_UPDATE

def change():
    lab_wel.setText('Удачи!!!')

#настройки главного окна
app = QApplication([])
main_window = QWidget()
main_window.resize(500, 500)
main_window.setWindowTitle("SmartProgramm")

#виджеты
lab_wel = QLabel("Добро пожаловать в умною, мощную, современную программу.\nВ ней содержится много чего...")
but_games = QPushButton("Игры")

#линии
lab_line = QHBoxLayout()
but_line = QHBoxLayout()
main_line = QVBoxLayout()

#присваивание виджетов к линиям
lab_line.addWidget(lab_wel, alignment=Qt.AlignCenter)
but_line.addWidget(but_games)
main_line.addLayout(lab_line)
main_line.addLayout(but_line)

#обработка
but_games.clicked.connect(TOTAL_UPDATE)
but_games.clicked.connect(change)
main_window.setLayout(main_line)
main_window.show()
app.exec_()