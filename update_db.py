import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psycopg2

from settings import connection_string, server_file_path, tables, screenshot_fields



def insert_into_database(filename, created_time):
    user_id = filename.split('_', maxsplit=1).pop(0)
    screen_time = int(created_time)
    print('USER: ', user_id)
    print('TIME: ', screen_time)
    conn = psycopg2.connect(host=connection_string['host'],
                            database=connection_string['database'],
                            user=connection_string['user'],
                            password=connection_string['password'])
    cursor = conn.cursor()
    query = f"""INSERT INTO {tables['screenshots']} ({screenshot_fields[0]}, {screenshot_fields[1]}) VALUES (%s, %s)"""
    cursor.execute(query, (user_id, screen_time))
    conn.commit()
    cursor.close()
    conn.close()



class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        created_time = os.path.getctime(event.src_path)
        insert_into_database(filename, created_time)



def start_watching():
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, server_file_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watching()
