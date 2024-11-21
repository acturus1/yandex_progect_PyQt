import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtCore import QProcess
from PyQt5 import QtGui

class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Терминал")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("background-color: #777c87;")

        # центральный виджет для отцентраливания и красоты
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # поле для ввода команды
        self.user_comand_input = QLineEdit(self)
        self.layout.addWidget(self.user_comand_input)

        # кнопка для запуска команды
        self.run_button = QPushButton("Выполнить команду", self)
        self.run_button.clicked.connect(self.run_command)
        self.layout.addWidget(self.run_button)

        style = """
            QPushButton {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        font = QtGui.QFont("Menlo", 16)  # Шрифт Arial, размер 14, жирный
        self.run_button.setFont(font)  # Применяем шрифт к кнопке
        self.run_button.setStyleSheet(style) # применяем стиль из style

        # гор. клавиша для кнопки запуска команды
        self.run_button.setShortcut('Return') 

        # список для вывода результатов
        self.terminal_command_list = QTextEdit(self)
        self.terminal_command_list.setReadOnly(True)
        self.layout.addWidget(self.terminal_command_list)
        self.terminal_command_list.setFont(font)  # Применяем шрифт к кнопке

        # собственно сам терминал
        self.process = QProcess(self)
        # кароч это делеться если терминал вывел стандартный ввод(текст) запустить terminal_output
        self.process.readyReadStandardOutput.connect(self.terminal_output) 

        self.current_directory = ""

    def run_command(self): # запускает команду
        command = self.user_comand_input.text() # берет команду из inputa 
        
        if command.strip():  # проверяем, что команда не пустая
            if command.startswith("cd "):  # cd 
                new_directory = command[3:].strip() # читстим до путя 
                if new_directory:  # если указан новый каталог
                    self.current_directory = new_directory  # запоминаем новый каталог
            else:
                # устанавливаем каталог 
                self.process.setWorkingDirectory(self.current_directory)
                self.process.start(command)  # отдаем терминалу команду для запуска
            self.user_comand_input.clear() # удаляем сделанную команду
            

    def terminal_output(self): # кароче эта функция выводит то что написал терминал
        output = self.process.readAllStandardOutput().data().decode() # прочитать содержимое
        self.terminal_command_list.append(output) # добавить в историю