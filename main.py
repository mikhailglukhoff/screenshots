import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import keyboard
import psycopg2
from PIL import ImageGrab

import credentials

key_listener_thread = None
key_listener_active = False


def take_screenshot():
    # Определяем имя файла с уникальным временным маркером
    filename = f"'screenshots_dir'/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    # Создаем скриншот с помощью библиотеки PIL
    screenshot = ImageGrab.grab()
    # Сохраняем скриншот
    screenshot.save(filename)
    print(f"Скриншот сохранен как {filename}")


def on_hotkey_press():
    # Действия при нажатии горячей клавиши (например, Ctrl + Alt + K)
    print("Горячая клавиша нажата")
    # Вызываем функцию создания скриншота
    take_screenshot()


def start_key_listener():
    global key_listener_thread, key_listener_active
    try:
        # Регистрация горячей клавиши
        keyboard.add_hotkey('ctrl+alt+k', on_hotkey_press)
    except Exception as e:
        print('Произошла ошибка при регистрации горячей клавиши:', e)

    # Функция-обработчик событий клавиатуры будет работать в отдельном потоке
    key_listener_thread = threading.Thread(target=keyboard_listener_thread)
    key_listener_active = True
    key_listener_thread.start()


def stop_key_listener():
    global key_listener_thread, key_listener_active
    keyboard.unhook_all()
    key_listener_active = False


def keyboard_listener_thread():
    # Запуск обработки событий клавиатуры в отдельном потоке
    while key_listener_active:
        keyboard.wait()


def authenticate(username, password):
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(host=credentials.connection_string['host'],
                                database=credentials.connection_string['database'],
                                user=credentials.connection_string['user'],
                                password=credentials.connection_string['password'])

        cursor = conn.cursor()

        # Выполняем SQL-запрос для поиска пользователя с данными логином и паролем
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (username, password))

        # Получаем результат запроса
        user_record = cursor.fetchone()

        if user_record:
            messagebox.showinfo("Успех", "Аутентификация прошла успешно")
            # Закрываем курсор и соединение с базой данных
            cursor.close()
            conn.close()
            # Скрыть поля ввода логина и пароля
            label_username.place_forget()
            entry_username.place_forget()
            label_password.place_forget()
            entry_password.place_forget()
            btn_submit.place_forget()
            # Вывести надпись "Online"
            label_online.place(x=150, y=10)
            # Показать кнопку "Выход"
            btn_exit.place(x=10, y=60)
            # Установка флага для начала отслеживания клавиш
            start_key_listener()

        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            # Очищаем поля ввода для повторного ввода
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)

    except Exception as error:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {error}")


def submit_credentials():
    username = entry_username.get()
    password = entry_password.get()

    # Проверяем, если поля не пустые
    if username and password:
        authenticate(username, password)
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите логин и пароль.")


def restart_program():
    stop_key_listener()
    python = sys.executable
    os.execl(python, python, *sys.argv)


def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        stop_key_listener()
        sys.exit()  # Полностью завершаем выполнение скрипта


# Создаем главное окно
root = tk.Tk()
root.title("LOGIN")
root.geometry("300x100")  # Задаем размеры окна
root.resizable(False, False)

# Обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)

# Создаем поля для ввода логина и пароля
label_username = tk.Label(root, text="Login:")
label_username.place(x=10, y=10)  # Задаем положение метки
entry_username = tk.Entry(root)
entry_username.place(x=80, y=10)  # Задаем положение поля ввода

label_password = tk.Label(root, text="Password:")
label_password.place(x=10, y=30)  # Задаем положение метки
entry_password = tk.Entry(root, show="*")  # Пароль будет отображаться как звездочки
entry_password.place(x=80, y=30)  # Задаем положение поля ввода

# Кнопка для отправки данных
btn_submit = tk.Button(root, text="Submit", command=submit_credentials)
btn_submit.place(x=10, y=60)  # Задаем положение кнопки

# Метка "Online"
label_online = tk.Label(root, text="Online")

# Кнопка "Выход"
btn_exit = tk.Button(root, text="Exit", command=restart_program)

# Запускаем цикл обработки событий
root.mainloop()
