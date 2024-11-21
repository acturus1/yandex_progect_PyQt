import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5 import QtGui
from browser import create_database, Browser
from text_edit import Redaktor_texta
from terminal import Terminal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #474a51;") 

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.browser_button = QPushButton('Открыть браузер', self)
        self.browser_button.clicked.connect(self.open_browser)
        layout.addWidget(self.browser_button)

        self.text_edit_button = QPushButton('Открыть блокнот', self)
        self.text_edit_button.clicked.connect(self.open_text_edit)
        layout.addWidget(self.text_edit_button)

        self.terminal_button = QPushButton('Открыть терминал', self)
        self.terminal_button.clicked.connect(self.open_terminal)
        layout.addWidget(self.terminal_button)

        style = """
            QPushButton {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        font = QtGui.QFont("Menlo", 16)  # Шрифт Arial, размер 14, жирный
        self.browser_button.setFont(font)  # Применяем шрифт к кнопке
        self.browser_button.setStyleSheet(style) # применяем стиль из style

        self.text_edit_button.setFont(font)
        self.text_edit_button.setStyleSheet(style)

        self.terminal_button.setFont(font)
        self.terminal_button.setStyleSheet(style)

    def open_browser(self): # функция которая открывает поиск
        self.poisk_windown = Browser()
        self.poisk_windown.show() 
    
    def open_text_edit(self):
        self.text_edit_windown = Redaktor_texta() # функция которая открывает текстовый редактор
        self.text_edit_windown.show()

    def open_terminal(self):
        self.terminal_windown = Terminal()
        self.terminal_windown.show()


if __name__ == '__main__':
    create_database()  # создание бд при запуске
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())