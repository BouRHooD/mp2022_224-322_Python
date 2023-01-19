"""
Источники информации: 
1) Разбор параметров командной строки в Python: https://jenyay.net/Programming/Argparse
2) Извлечение URL-адреса в Python: https://stackoverflow.com/questions/839994/extracting-a-url-in-python
3) Emoji: https://emojilo.com/ru/
4) Отслеживаем прогресс выполнения в Python: https://habr.com/ru/post/483400/
5) How To Take A Screenshot Using Python & Selenium?: https://www.lambdatest.com/blog/python-selenium-screenshots/
6) многопоточность python ожидание завершения всех потоков: https://translated.turbopages.org/proxy_u/en-ru.ru.0a6e851e-63c9b3c6-3ad97b7d-74722d776562/https/stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
"""

import os
import sys
import re  
import time
import keyboard  
import pandas  
import urllib.request
from utils import *
from progress.bar import IncrementalBar
from threading import Thread
from selenium import webdriver
from time import sleep

##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- #####
DEFAULT_PATH_DB         = "Project/databases/"
DEFAULT_PATH_FILES_URLS = "Project/files_urls/"
CURRENT_PATH_DB         = DEFAULT_PATH_DB
CURRENT_PATH_FILES_URLS = DEFAULT_PATH_FILES_URLS

MAX_FILES_DB            = 2
DEF_NAME_DB             = "app_db"
##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- ##### ----- #####

ALL_URLS = []
DATA_FOR_DB = []

WEB_DRIVER = None

def preparing_app_for_work():
    """ Подготавливаем приложения для нормальной работы (проверяем стандартные пути, создаем минимальные примеры, создаем БД) """

    # Проверяем наличие папок и создаем если их нет
    create_directory_if_not_exist(DEFAULT_PATH_DB)
    create_directory_if_not_exist(DEFAULT_PATH_FILES_URLS)

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
                # time.sleep(1)
                if is_esc: break; 

                # Ожидаем нажатия клавиши Esc для остановки выполенния цикла
                if keyboard.is_pressed("Esc"):
                    print()
                    print("------> Кнопка <Esc> была нажата, выходим из обработки файлов <------")
                    is_esc = True
                    break
                    
                # Проходимся по строкам и находим там URL
                path_file = os.path.join(root, name)
                lines_from_file = open(path_file).readlines()
                for line in lines_from_file:
                    if is_esc: break; 
                    
                    regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
                    matches = re.findall(regex, line)
                    if matches is None or len(matches) <= 0: continue; 

                    for sel_url in matches:
                        processed_urls.append([sel_url, path_file]) 

                bar.next()
            bar.finish()
    except Exception as ex:
        print(ex)
    
    ALL_URLS.extend(processed_urls) 

    print(f"➕ Добавлено ссылок: {len(processed_urls)}")
    print(f"🔗 Всего ссылок:     {len(ALL_URLS)}")

def get_data_from_urls():
    """ Потоки получения данных из ссылок"""
    try:
        WEB_DRIVER = webdriver.Chrome()

        create_threads_for_data()

        WEB_DRIVER.quit()
        WEB_DRIVER = None
    except Exception as ex:
        print(ex)

def create_threads_for_data():
    try:
        threads = []
        # Собираем список потоков
        for url, file_path in ALL_URLS:
            thread = Thread(target=get_data_info_from_url, args=(url, file_path,))
            threads.append(thread)
            thread.start()

        # Запускаем и ждес завершения
        for thread in threads:
            thread.join()
    except Exception as ex:
        print(ex)

def get_data_info_from_url(url_name, file_path):
    global DATA_FOR_DB
    if WEB_DRIVER is None:
        return

    # Проверяем соединение с сайтом
    response_status = 404  # 404 - Not Found
    try:
        opened_url = urllib.request.urlopen(url_name)
        response_status = opened_url.getcode()
    except urllib.error.HTTPError as http_ex:
        response_status = http_ex
    except Exception as ex:
         response_status = ex


    screenshot = 0
    # 200 - Ok
    if response_status == 200:
        try:
            WEB_DRIVER.get(url_name)
            sleep(1)
            base64 = WEB_DRIVER.get_screenshot_as_base64()
            screenshot = base64
        except Exception as ex:
            print(ex)

    DATA_FOR_DB.append([url_name, file_path, response_status, screenshot])

def update_db_info():
    """ Обновляем базу данных """
    # Добавляем данные в БД
    db_conn, db_cur = delete_old_and_create_new_db(CURRENT_PATH_DB, MAX_FILES_DB, DEF_NAME_DB)
    for data in DATA_FOR_DB:
        db_cur.execute("""INSERT INTO table_urls_stats (url_name, file_path, response_status, screenshot) VALUES (?,?,?,?)""", (data[0], data[1], data[2], data[3]))
    db_conn.commit()

    # Проверяем данные в БД
    dataframe = pandas.read_sql_query("SELECT * FROM table_urls_stats", db_conn)
    print(dataframe.head(15))   

def main_program_logic():
    """ Запускаем выполнение главной логики программы """
    try:
        preparing_app_for_work()
        get_args_from_console()
        get_urls_from_files()
        get_data_from_urls()
        update_db_info()
    except Exception as ex:
        print(ex)


def hello_word():
    print("#"*55) 
    print("💻 Приложение: Анализ URL ссылок из текстовых файлов")
    print("🧑‍ Автор:      Леонов Владислав Денисович 224-322")
    print("#"*55) 

# Точка входа в программу
if __name__ == "__main__":
    hello_word() 
    main_program_logic()