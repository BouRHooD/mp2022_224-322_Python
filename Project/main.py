"""
Источники информации: 
1) Разбор параметров командной строки в Python: https://jenyay.net/Programming/Argparse
2) Извлечение URL-адреса в Python: https://stackoverflow.com/questions/839994/extracting-a-url-in-python
3) Emoji: https://emojilo.com/ru/
4) Отслеживаем прогресс выполнения в Python: https://habr.com/ru/post/483400/
5) How To Take A Screenshot Using Python & Selenium?: https://www.lambdatest.com/blog/python-selenium-screenshots/
6) Многопоточность python ожидание завершения всех потоков: https://stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
7) Создание и просмотр HTML-файлов с помощью Python: https://www.geeksforgeeks.org/creating-and-viewing-html-files-with-python/
8) Python: Как создать оформленную HTML таблицу из pandas DataFrame: https://alexeyseleznev.wordpress.com/2020/04/30/python-%D0%BA%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%BB%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-html-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%83-%D0%B8%D0%B7-pa/
9) HTML to IMAGE using Python: https://stackoverflow.com/questions/60598837/html-to-image-using-python
10) Output images to html using python: https://stackoverflow.com/questions/7389567/output-images-to-html-using-python
11) How to add html styling in html page in python: https://stackoverflow.com/questions/31419888/how-to-add-html-styling-in-html-page-in-python
12) Как работать из PyCharm community c CSS: https://habr.com/ru/post/691892/
13) How can I take a screenshot/image of a website using Python?: https://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python
14) Лучший способ сделать снимок URL-адреса в Python: https://stackoverflow.com/questions/51000899/better-way-to-take-screenshot-of-a-url-in-python
15) HOWTO получение интернет-ресурсов с использованием пакета urllib: https://digitology.tech/docs/python_3/howto/urllib2.html?ysclid=ld40nfvga8813117223
16) How to store a jpg in an sqlite database with python: https://stackoverflow.com/questions/51301395/how-to-store-a-jpg-in-an-sqlite-database-with-python
17) How to Insert Image in SQLite using Python?: https://www.geeksforgeeks.org/how-to-insert-image-in-sqlite-using-python/
18) How to suppress console error/warning/info messages when executing selenium python scripts using chrome canary: https://stackoverflow.com/questions/46744968/how-to-suppress-console-error-warning-info-messages-when-executing-selenium-pyth
1() How to add image file in html using python: https://www.edureka.co/community/91405/how-to-add-image-file-in-html-using-python
"""

import os
import sys
import re  
import time
import keyboard  
import pandas  
import traceback
import urllib.request
from utils import *
from progress.bar import IncrementalBar
from threading import Thread
from selenium import webdriver

##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- #####
DEFAULT_PATH_DB         = "Project/databases/"
DEFAULT_PATH_FILES_URLS = "Project/files_urls/"
DEFAULT_PATH_HTML_PAGES = "Project/html_pages/"
CURRENT_PATH_DB         = DEFAULT_PATH_DB
CURRENT_PATH_FILES_URLS = DEFAULT_PATH_FILES_URLS
CURRENT_PATH_HTML_PAGES = DEFAULT_PATH_HTML_PAGES

MAX_FILES_DB            = 2
DEF_NAME_DB             = "app_db"
##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- #####

ALL_URLS = []
DATA_FOR_DB = []
DATAFRAME_PANDAS = pandas.DataFrame

GLOBAL_STATUS_BAR = None

def preparing_app_for_work():
    """ Подготавливаем приложения для нормальной работы (проверяем стандартные пути, создаем минимальные примеры, создаем БД) """

    # Проверяем наличие папок и создаем если их нет
    create_directory_if_not_exist(DEFAULT_PATH_DB)
    create_directory_if_not_exist(DEFAULT_PATH_FILES_URLS)
    create_directory_if_not_exist(DEFAULT_PATH_HTML_PAGES)

    # os.path.join(TEMP_DIR, "temp_SQLite.db")

# Для тестирования в terminal вставить: python Project/main.py "path_to_db" "path_to_files"
def get_args_from_console():
    """ Получаем параметры командной строки (получаем настройки приложения) """
    global CURRENT_PATH_DB, CURRENT_PATH_FILES_URLS

    argv_from_console = sys.argv
    if argv_from_console is None or len(argv_from_console) <= 1: 
        print(f'Параметры командной строки не получены')
        return

    print(f"Получены параметры командной строки: {argv_from_console}")
    if len(argv_from_console) >= 2: 
        CURRENT_PATH_DB = argv_from_console[1]
        print(f'📁 Новый путь: {CURRENT_PATH_DB=}')
    if len(argv_from_console) >= 3: 
        CURRENT_PATH_FILES_URLS = argv_from_console[2]
        print(f'📁 Новый путь: {CURRENT_PATH_FILES_URLS=}')

def get_urls_from_files():
    global ALL_URLS

    processed_urls = []
    try:
        print("'------> Нажмите <Esc> для завершения обработки файлов <------'")
        is_esc = False
        # Проходимся по путям 
        for root, dirs, files in os.walk(CURRENT_PATH_FILES_URLS):
            if is_esc: break; 

            # Проходимся по файлам и выводим прогресс
            bar = IncrementalBar(f'Обработаны файлы из {root}', max = len(files))
            for name in files:
                try:
                    # time.sleep(1)
                    if is_esc: break; 

                    # Ожидаем нажатия клавиши Esc для остановки выполенния цикла
                    if keyboard.is_pressed("Esc"):
                        print()
                        print("------> Кнопка <Esc> была нажата, выходим из обработки файлов <------")
                        is_esc = True
                        break
                        
                    # Проходимся по строкам и находим там URL
                    path_file = os.path.abspath(os.path.join(root, name))
                    lines_from_file = open(path_file).readlines()
                    for line in lines_from_file:
                        if is_esc: break; 
                        
                        regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
                        matches = re.findall(regex, line)
                        if matches is None or len(matches) <= 0: continue; 

                        for sel_url in matches:
                            processed_urls.append([sel_url, path_file]) 
                except Exception as ex:
                    traceback.print_exc(); print(ex); 

                bar.next()
            bar.finish()
    except Exception as ex:
        traceback.print_exc(); print(ex); 
    
    ALL_URLS.extend(processed_urls) 

    print(f"➕ Добавлено ссылок: {len(processed_urls)}")
    print(f"🔗 Всего ссылок:     {len(ALL_URLS)}")


def driver_setup(url_name: str) -> webdriver.Chrome:
    """ Для каждого потока необходимо создавать отдельный экземпляр, иначе будет делать скриншоты только для одного сайта """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")                  # Запускает Chrome в автономном режиме
    options.add_argument('--no-sandbox')                # Обход модели безопасности ОС
    options.add_argument('start-maximized')             # Максимальный размер экрана
    options.add_argument('disable-infobars')            # Отключаем плашку, что браузер управляется ПО
    options.add_argument("--disable-extensions")        # Отключаем вывод исключений в коносоль
    options.add_argument('--ignore-certificate-errors') # Игнорируем ошибку об сертификатах
    options.add_argument('--ignore-ssl-errors')         # Игнорируем ошибку об ssl (Secure Sockets Layer — уровень защищённых сокетов)
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('log-level=3')   
    options.add_argument('--headless')

    url_name_replaced = url_name.replace("/", "").replace("\\", "")
    path_log_file = f"Project/temp/_chrome_log_{url_name_replaced}.txt"
    LOCAL_WEB_DRIVER = webdriver.Chrome(chrome_options=options, service_log_path=path_log_file)
    return LOCAL_WEB_DRIVER

def get_data_from_urls():
    """ Потоки получения данных из ссылок"""
    try:
        # Собираем список потоков
        threads = []
        #drivers = []
        threads_bar = IncrementalBar(f'Инициализировано потоков', max = len(ALL_URLS))
        for url, file_path in ALL_URLS:
            #driver = driver_setup()
            thread = Thread(target=get_data_info_from_url, args=(url, file_path))
            #drivers.append(driver)
            threads.append(thread)
            threads_bar.next()
        threads_bar.finish()

        # Выполняем работу потоков
        create_threads_for_data(threads)

        # Завершаем работу драйверов
        #for driver in drivers:
        #    if driver is not None:
        #        driver.quit()
        #        driver = None

    except Exception as ex:
        traceback.print_exc(); print(ex); 

def create_threads_for_data(threads):
    try:
        # Очередь для потоков
        global GLOBAL_STATUS_BAR
        GLOBAL_STATUS_BAR = IncrementalBar(f'🚀 Обработано ссылок', max = len(ALL_URLS))

        start_time = time.time()

        
        # Запускаем и ждес завершения
        threads_bar = IncrementalBar(f'⚽ Запущено потоков', max = len(ALL_URLS))
        for thread in threads:
            thread.start()
            threads_bar.next()
        threads_bar.finish()

        for thread in threads:
            thread.join()

        """
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for url, file_path in ALL_URLS:
                future = executor.submit(get_data_info_from_url, url, file_path)
                futures.append(future)
    
            # ждем, когда закончат выполняться задачи
            for future in futures:
                future.result()
        """

        GLOBAL_STATUS_BAR.finish()
        GLOBAL_STATUS_BAR = None
        process_time = time.time() - start_time
        print(f"⏳ Обработка ссылок заняла: {process_time} s")

    except Exception as ex:
        traceback.print_exc(); print(ex); 


def get_data_info_from_url(url_name, file_path):
    # test
    #time.sleep(1)
    #GLOBAL_STATUS_BAR.next()
    #return

    global DATA_FOR_DB

    try:
        # Проверяем соединение с сайтом
        response_status = 404  # 404 - Not Found
        try:
            opened_url = urllib.request.urlopen(url_name)
            response_status = opened_url.getcode()
        except urllib.error.HTTPError as http_ex:
            response_status = http_ex
        except Exception as ex:
            response_status = ex

        # 200 - Ok
        # Получаем Скриншот веб-страницы
        screenshot = 0
        process_time = 0
        if response_status == 200:
            try:
                start_time = time.time()                                ## точка отсчета времени
                LOCAL_WEB_DRIVER = driver_setup(url_name)               # Открываем Chrome
                try:
                    # Самый наилучший вариант - инициализировать в разных потоках, так быстрее работает код
                    LOCAL_WEB_DRIVER.get(url_name)                          # Открываем страницу
                    time.sleep(1)                                           # Ждем загрузки 1 сек
                    bytes_image = LOCAL_WEB_DRIVER.get_screenshot_as_png()  # Делаем скриншот
                    screenshot = bytes_image                                # Запоминаем скриншот
                except Exception as ex:
                    traceback.print_exc(); print(ex); 
                LOCAL_WEB_DRIVER.quit()                                 # Закрываем Chrome
                process_time = time.time() - start_time                 ## собственно время работы программы
            except Exception as ex:
                traceback.print_exc(); print(ex); 

        DATA_FOR_DB.append([str(url_name), str(file_path), str(response_status), process_time, screenshot])
    except Exception as ex:
        traceback.print_exc(); print(ex); 

    try:
        if GLOBAL_STATUS_BAR is not None:
            GLOBAL_STATUS_BAR.next()
    except Exception as ex:
        pass

def update_db_info():
    """ Обновляем базу данных """
    # Добавляем данные в БД
    db_conn, db_cur = delete_old_and_create_new_db(CURRENT_PATH_DB, MAX_FILES_DB, DEF_NAME_DB)
    for data in DATA_FOR_DB:
        sql = """INSERT INTO table_urls_stats (url_name, file_path, response_status, process_time, screenshot) VALUES (?,?,?,?,?)"""
        db_cur.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
    db_conn.commit()

    # Проверяем данные в БД
    global DATAFRAME_PANDAS
    DATAFRAME_PANDAS = pandas.read_sql_query("SELECT * FROM table_urls_stats", db_conn)
    print(DATAFRAME_PANDAS.head(20))

def create_html_pages():
    try:
        # Получаем информацию из БД
        copy_df = DATAFRAME_PANDAS.copy()

        # Переводим байты в изображения для HTML
        import base64 
        data_screenshots_bytes_list = copy_df.screenshot
        data_screenshots_list = []
        threads_bar = IncrementalBar(f'🌄 Переведено изображений в формат HTML', max = len(data_screenshots_bytes_list))
        for screenshot_bytes in data_screenshots_bytes_list:
            try:
                base64_encoded_image = base64.b64encode(bytes(screenshot_bytes)).decode("utf-8")
                screenshot = '<img src="data:image/png;base64,{0}">'.format(base64_encoded_image)
                data_screenshots_list.append(screenshot)
            except:
                pass
            threads_bar.next()
        threads_bar.finish()
        copy_df.screenshot = data_screenshots_list

        # Из DataFrame to HTML 
        # (render_links=True - Преобразовывать url в hyperlinks) 
        html_table = copy_df.to_html(render_links=True, escape=False)
        # Возвращает формат для картинок  '&lt;img src="data:image/png;base64,(byte array)"&gt;' -----> <img src="data:image/jpg;base64, (byte array)">
        #html_table = str(html_table).replace("&lt;", "<").replace("&gt;", ">")
        html_string = f'''
        <html>
            <head>
                <title>HTML Dataframe from DB</title>
            </head>

            <link rel="stylesheet" type="text/css" href="df_style.css"/>
            <body>
                <h2>База данных</h2>
                {html_table}
            </body>
        </html>
        '''

        # Формируем 
        f = open(os.path.join(DEFAULT_PATH_HTML_PAGES, 'index.html'), 'w')  
        f.write(html_string)                # Записываем код в файл
        f.close()                           # Закрываем файл

        print("🌐 HTML страница сформирована на основе БД")
    except Exception as ex:
        traceback.print_exc(); print(ex); 

def main_program_logic():
    """ Запускаем выполнение главной логики программы """
    try:
        preparing_app_for_work()
        get_args_from_console()
        get_urls_from_files()
        get_data_from_urls()
        update_db_info()
        create_html_pages()
    except Exception as ex:
        traceback.print_exc(); print(ex); 


def hello_word():
    print() 
    print("#"*55) 
    print("💻 Приложение: Анализ URL ссылок из текстовых файлов")
    print("🧑‍ Автор:      Леонов Владислав Денисович 224-322")
    print("#"*55) 
    print() 

def end_word():
    print() 
    print("✅"*22) 
    print("✅   💻 Работа приложения завершена 💻    ✅")
    print("✅"*22) 
    print() 

# Точка входа в программу
if __name__ == "__main__":
    hello_word() 
    main_program_logic()
    end_word()