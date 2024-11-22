import sys
import sqlite3
import requests
from PyQt5 import QtGui
from bs4 import BeautifulSoup
from PyQt5.QtCore import QProcess, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, \
    QMessageBox, QTextEdit, QPushButton


def google_search(query):
    url = f'https://www.google.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) YandexBrowser/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Ошибка при выполнении запроса.')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a', href=True)
        if title and link:
            results.append((title.get_text(), link['href']))

    return results


def create_database():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_query(query):  # сохарнение в бд
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (query) VALUES (?)', (query,))
    conn.commit()
    conn.close()


def get_search_history():  # история поиска
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query FROM history ORDER BY id DESC')
    history = cursor.fetchall()
    conn.close()
    return [item[0] for item in history]


class BrowserWindow(QWebEngineView):  # окно с ссылкой
    def __init__(self, url):
        super(BrowserWindow, self).__init__()
        self.setUrl(QUrl(url))
        self.resize(1200, 800)
        self.show()


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        font = QtGui.QFont("Menlo", 16)  # Шрифт Arial, размер 14, жирный
        self.setStyleSheet("background-color: #777c87;")

        style_button = """
            QPushButton {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """
        style_input = """
            QLineEdit {
                background-color: #616161; 
                color: white; 
                font-size: 16px; 
                border: 1px solid #424242; 
            }
        """

        style_list = """
            QListWidget {
                background-color: #616161; 
                color: white; 
                font-size: 13px; 
                border: 1px solid #424242; 
            }
        """

        self.retern_button = QPushButton("Назад", self)
        self.retern_button.clicked.connect(self.undo_move)
        self.layout.addWidget(self.retern_button)
        self.retern_button.setFont(font)
        self.retern_button.setStyleSheet(style_button)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Введите запрос для поиска')
        self.layout.addWidget(self.search_input)
        self.search_input.setFont(font)  # Применяем шрифт к кнопке
        self.search_input.setStyleSheet(style_input)  # применяем стиль из style

        self.search_button = QPushButton('Поиск', self)
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)
        self.search_button.setShortcut('Return')
        self.search_button.setFont(font)  # Применяем шрифт к кнопке
        self.search_button.setStyleSheet(style_button)  # применяем стиль из style

        self.results_list = QListWidget(self)
        self.results_list.itemClicked.connect(self.open_link)
        self.layout.addWidget(self.results_list)
        self.results_list.setFont(font)  # Применяем шрифт к списку
        self.results_list.setStyleSheet(style_list)

        self.history_list = QListWidget(self)
        self.history_list.itemClicked.connect(self.perform_history_search)
        self.layout.addWidget(self.history_list)
        self.history_list.setFont(font)
        self.history_list.setStyleSheet(style_list)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        # загружаем историю поиска
        self.load_search_history()

    def perform_search(self):  # пишем то что нашел прасинг из гугла (10 ссылок с названиями)
        query = self.search_input.text()
        if query:
            print(f'Ищем такую штуку: {query}')
            results = google_search(query)
            if results:
                self.results_list.clear()
                for title, link in results:
                    self.results_list.addItem(f'{title} - {link}')
                save_query(query)
                self.load_search_history()  # обновляем историю поиска
            else:
                self.results_list.addItem('Ничего не найдено')

    def load_search_history(self):  # история поиска
        history = get_search_history()
        self.history_list.clear()
        for query in history:
            self.history_list.addItem(query)

    def open_link(self, item):  # открыть ссылку
        link = item.text().split(' - ')[1]  # обрезаем до ссылки
        if link.startswith('http'):  # проверяем, что с ссылкой все норм
            print(f'Открываем вот это: {link}')  # отладочное сообщение
            self.new_window = BrowserWindow(link)
            self.new_window.show()
        else:
            QMessageBox.critical(self, "Ошибка ", "Ссылка не рабочая")

    def perform_history_search(self, item):
        query = item.text()
        self.search_input.setText(query)  # текст -> в поле ввода
        self.perform_search()  # ищем в гугле по полю ввода

    def undo_move(self):
        self.terminal_windown = MainWindow()
        self.terminal_windown.show()
        self.hide()


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
        self.layout = QVBoxLayout(central_widget)

        self.retern_button = QPushButton("Назад", self)
        self.retern_button.clicked.connect(self.undo_move)
        self.layout.addWidget(self.retern_button)

        # само содержание файла которое можно редактировать 
        self.redact_text = QTextEdit(self)
        self.layout.addWidget(self.redact_text)

        # кнопки для работы с файлом
        self.open_button = QPushButton('Открыть', self)
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)

        self.new_button = QPushButton('Новый', self)
        self.new_button.clicked.connect(self.new_file)
        self.layout.addWidget(self.new_button)

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

        self.open_button.setFont(font)  # стили для каждых кнопок
        self.open_button.setStyleSheet(style)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet(style)
        self.new_button.setFont(font)
        self.new_button.setStyleSheet(style)
        self.retern_button.setFont(font)
        self.retern_button.setStyleSheet(style)

    def open_file(self):
        file_name, xren1_0 = QFileDialog.getOpenFileName(self, 'Открыть файл', '',
                                                         'Text file (*.txt);;Python file (*.py)')
        # в строке сверху ОБЯЗАТЕЛЬНО должно стоять что нибудь у меня это xren1_0 иначе программа не будет работать, потому что это тип файла
        file_name_title = file_name.split('/')[-1]  # обрезаем полное расплоложение файла
        self.setWindowTitle(file_name_title)  # делаем красивую верхушку
        if file_name:
            try:  # проверяем на ошибку при открытии
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.redact_text.setText(content)
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть файл: {e}')

    def save_file(self):
        file_name, xren2_0 = QFileDialog.getSaveFileName(self, 'Сохранить файл', '',
                                                         'Text file (*.txt);;Python file (*.py)')

        if file_name:
            try:  # проверяем на ошибку при сохранении
                with open(file_name, 'w', encoding='utf-8') as file:
                    content = self.redact_text.toPlainText()
                    file.write(content)
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить файл: {e}')

    def new_file(self):
        self.setWindowTitle('Новый файл')  # обозначаем что файл новый
        self.redact_text.clear()  # очистили все что было (надо бы добавить чтоб он сохранял перед закрытием)

    def undo_move(self):
        self.terminal_windown = MainWindow()
        self.terminal_windown.show()
        self.hide()


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

        self.retern_button = QPushButton("Назад", self)
        self.retern_button.clicked.connect(self.undo_move)
        self.layout.addWidget(self.retern_button)

        style_input = """
            QLineEdit {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        # поле для ввода команды
        self.user_comand_input = QLineEdit(self)
        self.layout.addWidget(self.user_comand_input)

        font = QtGui.QFont("Menlo", 16)  # Шрифт Arial, размер 14, жирный

        self.user_comand_input.setFont(font)  # Применяем шрифт к кнопке
        self.user_comand_input.setStyleSheet(style_input)  # применяем стиль из style

        # кнопка для запуска команды
        self.run_button = QPushButton("Выполнить команду", self)
        self.run_button.clicked.connect(self.run_command)
        self.layout.addWidget(self.run_button)

        self.instruction_button = QPushButton("Инструкция", self)
        self.instruction_button.clicked.connect(self.instruction)
        self.layout.addWidget(self.instruction_button)

        self.clear_button = QPushButton("Очистить", self)
        self.clear_button.clicked.connect(self.clear_text)
        self.layout.addWidget(self.clear_button)

        style = """
            QPushButton {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        self.run_button.setFont(font)  # Применяем шрифт к кнопке
        self.run_button.setStyleSheet(style)  # применяем стиль из style

        self.instruction_button.setFont(font)  # Применяем шрифт к кнопке
        self.instruction_button.setStyleSheet(style)  # применяем стиль из style

        self.clear_button.setFont(font)  # Применяем шрифт к кнопке
        self.clear_button.setStyleSheet(style)  # применяем стиль из style

        self.retern_button.setFont(font)  # Применяем шрифт к кнопке
        self.retern_button.setStyleSheet(style)  # применяем стиль из style

        # гор. клавиша для кнопки запуска команды
        self.run_button.setShortcut('Return')

        style_list = """
            QTextEdit {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        # список для вывода результатов
        self.terminal_command_list = QTextEdit(self)
        self.terminal_command_list.setReadOnly(True)
        self.layout.addWidget(self.terminal_command_list)

        self.terminal_command_list.setFont(font)  # Применяем шрифт к кнопке
        self.terminal_command_list.setStyleSheet(style_list)  # применяем стиль из style

        # собственно сам терминал
        self.process = QProcess(self)
        # кароч это делеться если терминал вывел стандартный ввод(текст) запустить terminal_output
        self.process.readyReadStandardOutput.connect(self.terminal_output)

        self.current_directory = ""

    def run_command(self):  # запускает команду
        command = self.user_comand_input.text()  # берет команду из inputa

        if command.strip():  # проверяем, что команда не пустая
            if command.startswith("cd "):  # cd 
                new_directory = command[3:].strip()  # читстим до путя
                if new_directory:  # если указан новый каталог
                    self.current_directory = new_directory  # запоминаем новый каталог
            else:
                # устанавливаем каталог 
                self.process.setWorkingDirectory(self.current_directory)
                self.process.start(command)  # отдаем терминалу команду для запуска

            if command == 'clear':
                self.clear_text()

            self.user_comand_input.clear()  # удаляем сделанную команду

    def terminal_output(self):  # кароче эта функция выводит то что написал терминал
        output = self.process.readAllStandardOutput().data().decode()  # прочитать содержимое
        self.terminal_command_list.append(output)  # добавить в историю

    def instruction(self):  # функция для запуска окна с инттрукцией
        self.new_window = Instruction()
        self.new_window.show()

    def clear_text(self):  # функция для очистки текста
        self.terminal_command_list.clear()

    def undo_move(self):  # кнопка назад
        self.terminal_windown = MainWindow()  # создаем экземпляр класса
        self.terminal_windown.show()  # показываение старого окна
        self.hide()  # скрывание текущего


class Instruction(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Текстовое поле в PyQt5")
        self.setGeometry(100, 100, 600, 400)  # Позиция и размер окна

        self.setStyleSheet("background-color: #777c87;")

        # Создаем центральный виджет и устанавливаем его
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный layout
        layout = QVBoxLayout(central_widget)

        # Создаем текстовое поле
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("При использовании терминала учитывайте то что команда cd рабоатет только на дерикторию вверх,\
        если использовать ее на дерикторию вниз, она выведет ошибку.\
        так же если терминал не выполняет команду - он завис, просто закройте терминал и откройте его снова")  # инструкция для пользователя

        style = """
            QTextEdit {
                background-color: #61636f;
                color: white; 
                border: none;
                border-radius: 5px 
            }
        """

        font = QtGui.QFont("Menlo", 16)  # Шрифт Arial, размер 14, жирный
        self.text_edit.setFont(font)  # Применяем шрифт к кнопке
        self.text_edit.setStyleSheet(style)  # применяем стиль из style

        # Добавляем текстовое поле в layout
        layout.addWidget(self.text_edit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #474a51;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.browser_button = QPushButton('Открыть браузер', self)
        self.browser_button.clicked.connect(self.open_browser)
        self.layout.addWidget(self.browser_button)

        self.text_edit_button = QPushButton('Открыть блокнот', self)
        self.text_edit_button.clicked.connect(self.open_text_edit)
        self.layout.addWidget(self.text_edit_button)

        self.terminal_button = QPushButton('Открыть терминал', self)
        self.terminal_button.clicked.connect(self.open_terminal)
        self.layout.addWidget(self.terminal_button)

        self.exit_button = QPushButton('Выход', self)
        self.exit_button.clicked.connect(self.close_windown)
        self.layout.addWidget(self.exit_button)

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
        self.browser_button.setStyleSheet(style)  # применяем стиль из style

        self.text_edit_button.setFont(font)
        self.text_edit_button.setStyleSheet(style)

        self.terminal_button.setFont(font)
        self.terminal_button.setStyleSheet(style)

        self.exit_button.setFont(font)
        self.exit_button.setStyleSheet(style)

    def open_browser(self):  # функция которая открывает поиск
        self.poisk_windown = Browser()
        self.poisk_windown.show()
        self.hide()

    def open_text_edit(self):
        self.text_edit_windown = Redaktor_texta()  # функция которая открывает текстовый редактор
        self.text_edit_windown.show()
        self.hide()

    def open_terminal(self):
        self.terminal_windown = Terminal()
        self.terminal_windown.show()
        self.hide()

    def close_windown(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    # create_database()  # создание бд при запуске
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
