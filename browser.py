import requests
from bs4 import BeautifulSoup
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, QMessageBox
from PyQt5 import QtGui
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

def save_query(query): # сохарнение в бд
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (query) VALUES (?)', (query,))
    conn.commit()
    conn.close()

def get_search_history(): # история поиска
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query FROM history ORDER BY id DESC')
    history = cursor.fetchall()
    conn.close()
    return [item[0] for item in history]


class BrowserWindow(QWebEngineView): # окно с ссылкой 
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
            QListWidget {
                font-size: 16px; 
            }
        """

        style_list = """
            QLineEdit {
                background-color: #616161; 
                color: white; 
                font-size: 16px; 
                border: 1px solid #424242; 
            }
        """

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Введите запрос для поиска')
        self.layout.addWidget(self.search_input)
        self.search_input.setFont(font)  # Применяем шрифт к кнопке
        self.search_input.setStyleSheet(style_input) # применяем стиль из style
        
        self.search_button = QPushButton('Поиск', self)
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)
        self.search_button.setFont(font)  # Применяем шрифт к кнопке
        self.search_button.setStyleSheet(style_button) # применяем стиль из style

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

    def perform_search(self): # пишем то что нашел прасинг из гугла (10 ссылок с названиями)
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
                self.results_list.addItem('Ничего не найдено')

    def load_search_history(self): # история поиска
        history = get_search_history()
        self.history_list.clear()
        for query in history:
            self.history_list.addItem(query)

    def open_link(self, item): # открыть ссылку 
        link = item.text().split(' - ')[1] # обрезаем до ссылки 
        if link.startswith('http'):  # проверяем, что с ссылкой все норм
            print(f'Открываем вот это: {link}') # отладочное сообщение
            self.new_window = BrowserWindow(link)
            self.new_window.show()
        else:
            QMessageBox.critical(self, "Ошибка ", "Ссылка не рабочая")

    def perform_history_search(self, item):
        query = item.text()
        self.search_input.setText(query) # текст -> в поле ввода
        self.perform_search()  # ищем в гугле по полю ввода