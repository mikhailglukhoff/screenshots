import sys

# sys.path.append('/home/mikhail/PycharmProjects/screenshots/.venv/lib/python3.10/site-packages')
import keyboard


def start_key_listener():
    def on_key_press(event):
        print('Нажата клавиша:', event.name)

    # Регистрируем обработчик события нажатия клавиш
    keyboard.on_press(on_key_press)

    # Запускаем "бесконечный" цикл для удержания программы активной
    while True:
        pass
