## Настройки

Все настройки находятся в settings.py.

Строка подключения к PostgreSQL:
`connection_string = {
'host': "HOST",
'database': "DATABASE_NAME",
'user': "DB_USER",
'password': "PASS"
}`

Имена таблиц в БД для авторизации и хранения скриншотов:
`tables = {'users': 'users', 'screenshots': 'screenshots'}`

Поля БД для авторизации:
`login_fields = ('user_id', 'password')`

Поля БД для хранения данных по скриншотам:
`screenshot_fields = ('user_id', 'screen_time')`

Путь для хранения скриншотов у клиента:
`screenshots_directory = r'C:\Users\Professional\PycharmProjects\screenshots\screenshots_dir'`

Комбинация клавиш для создания скриншота:
`hot_key = 'ctrl+alt+k'`

Путь для хранения скриншотов на сервере:
`server_file_path = r'C:\Users\Professional\PycharmProjects\screenshots\server_dir'`

Настройки сервера для сокетного соединения:
`server_host_port = ('localhost', 12345)`

Интервал группировки скриншотов:
`screenshot_interval = 180`

Интервал для анализа задержки отправки скриншотов (Unix-time):
`start_time, end_time = (1712689230, 1712689500)`

## Клиентская часть

Запускаем [main.py](main.py), вводим логин и пароль (хранятся в _screenshot_db.public.users_).

После успешной авторизации `handle_hot_key` ожидает нажатия комбинации _hot_key_, сохраняет скриншот локально и отправляет
на сервер через сокетное соединение.

Остановка по нажатию кнопки _Log out_.

## Серверная часть

Для работы должны быть запущены:

[server_socket.py](server_socket.py) - получает имя файла, затем его содержимое

[update_db.py](update_db.py) - отслеживает новые файлы, получает имя пользователя из имени файла и время создания файла из метаданных, затем отправляет их в _screenshot_db.public.screenshots_.



## Анализ 

Для анализа должен быть запущен [analyse_db.py](analyse_db.py).

В [settings.py](settings.py) нужно указать время начала и окончания периода анализа.

Результат анализа в виде `{'group_1': {'user1': 0, 'user2': 30, 'user3': 56}, 'group_2': {'user4': 0, 'user5': 1}}`

### рабочая инфа

компиляция exe-шника для юзера:

