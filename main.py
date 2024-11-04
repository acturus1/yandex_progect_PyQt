import sys
import requests
from bs4 import BeautifulSoup
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

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

def save_query(query):
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (query) VALUES (?)', (query,))
    conn.commit()
    conn.close()

def get_search_history():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query FROM history ORDER BY id DESC')
    history = cursor.fetchall()
    conn.close()
    return [item[0] for item in history]

class BrowserWindow(QWebEngineView):
    def __init__(self, url):
        super(BrowserWindow, self).__init__()
        self.setUrl(QUrl(url))
        self.resize(1200, 800)
        self.show()

class Poisk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Введите запрос для поиска')
        self.layout.addWidget(self.search_input)
        
        self.search_button = QPushButton('Поиск', self)
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)
        
        self.results_list = QListWidget(self)
        self.results_list.itemClicked.connect(self.open_link)
        self.layout.addWidget(self.results_list)

        self.history_list = QListWidget(self)
        self.history_list.itemClicked.connect(self.perform_history_search)
        self.layout.addWidget(self.history_list)

        container = QWidget()
        container.setLayout(self.layout)
        
        self.setCentralWidget(container)

        # загружаем историю поиска
        self.load_search_history()

    def perform_search(self):
        query = self.search_input.text()
        if query:
            print(f'Ищем такую штуку: {query}')
            results = google_search(query)
            if results:
                self.results_list.clear()
                for title, link in results:
                    self.results_list.addItem(f'{title} - {link}')
                save_query(query) 
                self.load_search_history() # обновляем историю поиска
            else:
                print('Ничего не найдено')

    def load_search_history(self):
        history = get_search_history()
        self.history_list.clear()
        for query in history:
            self.history_list.addItem(query)

    def open_link(self, item):
        link = item.text().split(' - ')[1]
        if link.startswith('http'):  # проверяем, что с ссылкой все норм
            print(f'Открываем вот это: {link}')
            self.new_window = BrowserWindow(link)
            self.new_window.show() 
        else:
            print('ссылка не рабочая')

    def perform_history_search(self, item):
        query = item.text()
        self.search_input.setText(query) # текс -> в поле ввода
        self.perform_search()  # Ищем текст по полю ввода

class Redaktor_texta(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Новый файл')
        self.setGeometry(100, 100, 600, 400)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.browser_button = QPushButton('Открыть браузер', self)
        self.browser_button.clicked.connect(self.open_browser)
        layout.addWidget(self.browser_button)

        self.browser_button = QPushButton('Открыть обрезанный блокнот(да я гений епта)', self)
        self.browser_button.clicked.connect(self.open_text_edit)
        layout.addWidget(self.browser_button)

    def open_browser(self):
        self.poisk_windown = Poisk()
        self.poisk_windown.show() 
    
    def open_text_edit(self):
        self.text_edit_windown = Redaktor_texta()
        self.text_edit_windown.show()

if __name__ == '__main__':
    create_database()  # создание бд при запуске
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
