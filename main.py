import requests
from bs4 import BeautifulSoup

def google_search(query):
    # ссылка для поиска
    url = f"https://www.google.com/search?q={query}"
    
    # важная хрень если requests будет выдавать ошибку поменять 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # проверка на ошибку
    if response.status_code != 200:
        print("Ошибка при выполнении запроса.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # берем ссылки из запроса который сделался из url
    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a', href=True)
        if title and link:
            results.append((title.get_text(), link['href']))
    
    return results

def main():
    query = input("Введите текст для поиска: ")
    
    # Получаем результаты поиска
    results = google_search(query)
    
    if not results:
        print("Результаты не найдены.")
        return
    
    print("\nРезультаты поиска:")
    for i, (title, link) in enumerate(results):
        # выводим что он там нашел 
        print(f"{i + 1}: {title} - {link}")
    
    # пользователь выбирает 
    try:
        choice = int(input("\nВыберите номер сайта для перехода: ")) - 1
        
        if 0 <= choice < len(results):
            print(f"Вы выбрали: {results[choice][1]}")
            return results[choice][1]
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")

# часть Qt приложения 

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        url_seaching = main()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url_seaching))

        self.setCentralWidget(self.browser)
        self.showMaximized()

        # это панель из кнопок Назад вперед и обновить страницу а еще для ввода url
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Кнопка назад
        back_btn = QAction('Назад', self)
        back_btn.triggered.connect(self.browser.back)
        self.toolbar.addAction(back_btn)

        # Кнопка вперед
        forward_btn = QAction('Вперед', self)
        forward_btn.triggered.connect(self.browser.forward)
        self.toolbar.addAction(forward_btn)

        # Кнопка обновить
        reload_btn = QAction('Обновить', self)
        reload_btn.triggered.connect(self.browser.reload)
        self.toolbar.addAction(reload_btn)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('...')
    window.show()
    sys.exit(app.exec_())