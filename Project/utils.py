def create_directory_if_not_exist(in_path: str):
    """ Проверяем наличие пути и создаем его, если он не существует """
    import os
    if not os.path.exists(in_path):
        os.mkdir(in_path)
        print(f'➕📁 Создана директория: {in_path=}')

def delete_old_and_create_new_db(in_path_to_dir_db: str, max_files_db: int, def_name_db: str):
    """ Удаляем старую базу данных и создаем новую"""
    try:

        # Находим пути до файлов БД
        import os
        paths_to_db = []
        for root, dirs, files in os.walk(in_path_to_dir_db):
            for name in files:
                if ".db" in name:
                    paths_to_db.append(os.path.join(root, name))
        
        # Удаляем лишние файлы БД (оставляет поздние файлы)
        if (len(paths_to_db) >= max_files_db):
            for file_db in paths_to_db:
                if len(paths_to_db) <= max_files_db:
                    os.remove(file_db)
                    paths_to_db.remove(file_db)

        # Создаем новый файл БД
        import sqlite3
        import datetime
        db_name = os.path.join(in_path_to_dir_db, f"{def_name_db}_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.db")
        db_conn = sqlite3.connect(db_name)
        db_cur = db_conn.cursor()
        db_cur.execute("CREATE TABLE IF NOT EXISTS table_urls_stats"
        "(id integer primary key,"
        "url_name varchar(1000),"
        "file_path varchar(1000),"
        "response_status varchar(1000),"
        "process_time REAL,"
        "screenshot BLOB)")

        print(f"💌 Создана БД и БД подключена к приложению")
        return db_conn, db_cur


    except Exception as ex:
        print(ex)
