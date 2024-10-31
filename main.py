import sys
import requests
from bs4 import BeautifulSoup
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) YandexBrowser/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Ошибка при выполнении запроса.")
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
        self.show()  # Убедитесь, что окно отображается

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введите запрос для поиска")
        self.layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Поиск", self)
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
            print(f"Ищем такую штуку: {query}")
            results = google_search(query)
            if results:
                self.results_list.clear()
                for title, link in results:
                    self.results_list.addItem(f"{title} - {link}")
                save_query(query) 
                self.load_search_history() # обновляем историю поиска
            else:
                print("Ничего не найдено")

    def load_search_history(self):
        history = get_search_history()
        self.history_list.clear()
        for query in history:
            self.history_list.addItem(query)

    def open_link(self, item):
        link = item.text().split(' - ')[1]
        if link.startswith("http"):  # проверяем, что с ссылкой все норм
            print(f"Открываем вот это: {link}")
            self.new_window = BrowserWindow(link)
            self.new_window.show() 
        else:
            print("ссылка не рабочая")

    def perform_history_search(self, item):
        query = item.text()
        self.search_input.setText(query) # текс -> в поле ввода
        self.perform_search()  # Ищем текст по полю ввода

if __name__ == '__main__':
    create_database()  # создание бд при запуске
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())