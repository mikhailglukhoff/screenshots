import os
import sys

import psycopg2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from settings import *

is_authorised = False


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.setFixedSize(300, 300)
        self.layout = QVBoxLayout()

        # Поле статуса
        self.label_status = QLabel("Offline")
        self.layout.addWidget(self.label_status)

        # Поля ввода имени и пароля
        self.label_username = QLabel("Username:")
        self.entry_username = QLineEdit()
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.entry_username)

        self.label_password = QLabel("Password:")
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.entry_password)

        # Кнопки Submit и Exit
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.clicked.connect(self.submit_credentials)
        self.layout.addWidget(self.btn_submit)

        self.btn_exit = QPushButton("Log out")
        self.btn_exit.hide()
        self.btn_exit.clicked.connect(self.restart_program)
        self.layout.addWidget(self.btn_exit)

        self.setLayout(self.layout)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def submit_credentials(self):
        global is_authorised
        username = self.entry_username.text()
        password = self.entry_password.text()
        if username and password:
            try:
                # Подключаемся к базе данных
                conn = psycopg2.connect(host=connection_string['host'],
                                        database=connection_string['database'],
                                        user=connection_string['user'],
                                        password=connection_string['password'])
                cursor = conn.cursor()

                # Выполняем SQL-запрос для проверки имени пользователя и пароля
                cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (username, password))

                # Получаем результат запроса
                user_record = cursor.fetchone()

                if user_record:
                    # Авторизация успешна, изменяем статус и скрываем окно авторизации
                    self.label_status.setText("Online")
                    self.label_username.hide()
                    self.entry_username.hide()
                    self.label_password.hide()
                    self.entry_password.hide()

                    self.btn_submit.hide()
                    self.btn_exit.show()
                    is_authorised = True
                else:
                    # Неверное имя пользователя или пароль
                    QMessageBox.warning(self, "Error", "Invalid username or password")
                    self.entry_username.clear()
                    self.entry_password.clear()
                    is_authorised = False

                # Закрываем курсор и соединение с базой данных
                cursor.close()
                conn.close()

            except Exception as error:
                # Ошибка подключения к базе данных
                QMessageBox.showerror("Error", f"Error connecting to the database: {error}")
        else:
            # Неверное имя пользователя или пароль
            QMessageBox.warning(self, "Error", "Invalid username or password")
            self.entry_username.clear()
            self.entry_password.clear()
            is_authorised = False
