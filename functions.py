from tkinter import messagebox
import os

from keyboard_listener import on_key_press
import credentials

import sys

sys.path.append('/home/mikhail/PycharmProjects/screenshots/.venv/lib/python3.10/site-packages')
import tkinter as tk
import psycopg2

# def take_screenshot(file_path):
#     # Делаем скриншот текущего экрана
#     screenshot = pyautogui.screenshot()
#
#     # Сохраняем скриншот в указанный файл
#     screenshot.save(file_path)
#
#     print(f"Скриншот сохранен в файле: {file_path}")
#
#
# if __name__ == "__main__":
#     file_path = "screenshot.png"  # Путь и имя файла, куда будет сохранен скриншот
#     take_screenshot(file_path)


def start_app():
    def authenticate(username, password):
        try:
            # Подключаемся к базе данных
            connection = credentials.conn

            cursor = connection.cursor()

            # Выполняем SQL-запрос для поиска пользователя с данными логином и паролем
            cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (username, password))

            # Получаем результат запроса
            user_record = cursor.fetchone()

            if user_record:
                messagebox.showinfo("Успех", "Аутентификация прошла успешно")
                # Закрываем курсор и соединение с базой данных
                cursor.close()
                connection.close()
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

                # Начать ожидание комбинации клавиш для выполнения другой функции
                # on_key_press(root)  # Запускаем функцию из файла keyboard_listener под root

            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
                # Очищаем поля ввода для повторного ввода
                entry_username.delete(0, tk.END)
                entry_password.delete(0, tk.END)

        except (Exception, psycopg2.Error) as error:
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
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Создаем главное окно
    root = tk.Tk()
    root.title("LOGIN")
    root.geometry("300x100")  # Задаем размеры окна
    root.resizable(False, False)

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
