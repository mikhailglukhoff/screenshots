import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psycopg2

from settings import connection_string, server_file_path, tables


# Функция для отправки имени файла в базу данных PostgreSQL
def insert_into_database(filename):
    conn = psycopg2.connect(host=connection_string['host'],
                            database=connection_string['database'],
                            user=connection_string['user'],
                            password=connection_string['password'])
    cursor = conn.cursor()
    query = f"""INSERT INTO {tables['tables']} (filename) VALUES (%s)"""
    cursor.execute(query, (filename,))
    conn.commit()
    cursor.close()
    conn.close()


# Обработчик событий файловой системы
class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        insert_into_database(filename)


# Функция для запуска монитора папки
def start_watching():
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, server_file_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watching()
