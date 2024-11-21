from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt5 import QtGui

class Redaktor_texta(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Новый файл')
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("background-color: #777c87;") 

        # центральный виджет для отцентраливания и красоты
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # само содержание файла которое можно редактировать 
        self.redact_text = QTextEdit(self)
        layout.addWidget(self.redact_text)

        # кнопки для работы с файлом
        self.open_button = QPushButton('Открыть', self)
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.new_button = QPushButton('Новый', self)
        self.new_button.clicked.connect(self.new_file)
        layout.addWidget(self.new_button)

        # горячие клавиши на английскую раскладку
        self.open_button.setShortcut('Ctrl+O') 
        self.save_button.setShortcut('Ctrl+S')
        self.new_button.setShortcut('Ctrl+N')

        # горячие клавиши на русскую раскладку
        self.open_button.setShortcut('Ctrl+Щ') 
        self.save_button.setShortcut('Ctrl+Ы')
        self.new_button.setShortcut('Ctrl+Т')

        font = QtGui.QFont("Menlo", 16)

        style = """
            QPushButton {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        self.open_button.setFont(font)
        self.open_button.setStyleSheet(style)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet(style)
        self.new_button.setFont(font)
        self.new_button.setStyleSheet(style)

    def open_file(self):
        file_name, xren1_0 = QFileDialog.getOpenFileName(self, 'Открыть файл', '', 'Text file (*.txt);;Python file (*.py)') 
        # в строке сверху ОБЯЗАТЕЛЬНО должно стоять что нибудь у меня это xren1_0 иначе программа не будет работать, потому что это тип файла
        file_name_title = file_name.split('/')[-1] # обрезаем полное расплоложение файла 
        self.setWindowTitle(file_name_title) # делаем красивую верхушку
        if file_name:
            try: # проверяем на ошибку при открытии 
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.redact_text.setText(content)
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть файл: {e}')

    def save_file(self):
        file_name, xren2_0 = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Text file (*.txt);;Python file (*.py)')

        if file_name:
            try: # проверяем на ошибку при сохранении 
                with open(file_name, 'w', encoding='utf-8') as file:
                    content = self.redact_text.toPlainText()
                    file.write(content)
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить файл: {e}')

    def new_file(self):
        self.setWindowTitle('Новый файл') # обозначаем что файл новый
        self.redact_text.clear() # очистили все что было (надо бы добавить чтоб он сохранял перед закрытием)