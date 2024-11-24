# Эмулятор операционной системы
Мой проект по PyQt5 во время обучения в яндекс лицее (Савкин Виктор)

## Установка (Linux, Unix)
У вас должны быть установлен Python версии 3.9 или выше

1. Клонирование репозитория 

```git clone https://github.com/viktorsavkin333/yandex_progect_PyQt.git```

2. Установка библиотек

```pip3 install -r requirements.txt``` или ```pip install -r requirements.txt```

3. Запуск скрипта 

```python3 main.py``` или ```python main.py```

## Использование 

1. После запуска перед вами открываеться окно в нем есть 4 кнопки:
    1. Кнопка 'Открыть браузер'
    2. Кнопка 'Открыть блокнот'
    3. Кнопка 'Открыть терминал'
    4. Кнопка 'Выход'

2. Выбираете кнопку затем вас перекидывает в одно из 3 окон

3. Окно браузера:
    1. У вас появляеться окошко: в поле вы вводите ссылку затем нажимаете найти в списке
    ниже у вас выбор из вариантов вы выбираете 1 и у вас открываеться окно с браузером
    2. В списке в самом низу у вас история поиска
    3. Вы вибираете ссылку и у вас открываеться окно 
    4. Чтобы выйти из окна браузера закройте его, затем закройте окно с поиском нажав 
    кнопку назад

4. Окно текстового редактора:
    1. Кнопка открыть или же сочетание "Ctrl+O": открывает файл 
    который вы можете выбрать из вашего компьютера
    2. Кнопка сохранить или же сочетание "Ctrl+S": сохраняет текущий файл
    3. Кнопка новый или же сочетание "Ctrl+N": создает новый файл
    4. Чтобы выйти нажмите кнопку назад

5. Окно терминала: 
    1. В поле ввода введите команду которую хотите выполнить
    2. Затем нажмите выполнить или же нажмите Enter
    3. После выполнения команда появится в списке 
    4. Кнопка очистить чистит историю команд
    5. Обязательно перед использованием прочитать инструкцию!
    6. Чтобы выйти нажмите кнопку назад

# Описание реализации
1. Браузер
Браузер я поделил на 3 этапа: 
1 - поиск ссылок
2 - обработка ссылок 
3 - открытие ссылки

Начнем с 1 - поиска ссылок: в функции google_search с помощью парсинга ищуться ссылки 
с самого гугла, затем обрабатываются в процессе номер 2:
так же происходит в функции google_search: береться ссылка и название страницы 
и сохраняются в виде кортежа в списке result, затем в функции perform_search 
эти ссылки выводяться пользователю в виде списка с кнопками.
ну и показ ссылки в отдельном окне: браузере с помощью QWebEngineView


2. Текстовый редактор
1 - открытие файла
2 - сохранение файла

1 - открытие файла происходит с помощью QFileDialog.getOpenFileName - где берться имя файла
и открываеться на чтение, так же береться имя и обрезаеться для заголовка страницы:
поддерживает файлы типа .py и .txt
2 - сохранение файла так же происходит с помощью открытия файла но уже не запись: береться все 
содержание файла и записываеться, затем сохраняеться 
Так же присутствует создание нового пустого файла 


3. Терминал

readyReadStandardOutput - читает вывод терминаал 
terminal_output - записывает вывод терминала
Instruction - класс с инструкцией 
clear_text - чистит вывод
run_command - обрабатывает команду взятую из поля ввода и обрабатывает ее: если cd то
перейти в дерикторию с помощью setWorkingDirectory так же обрабатываеться команда 
clea: просто выполняет функцию clear_text


## Документация

1. [Документация по Python](https://docs.python.org/3/index.html)

2. [Документация по Qt](https://doc.qt.io) 

3. [Документация по bs4](https://beautiful-soup-4.readthedocs.io)
