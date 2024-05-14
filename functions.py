import datetime
import keyboard
import pyautogui
import os
import socket
import time
import logging
import settings

from settings import hot_key, screenshots_directory
from dotenv import load_dotenv

load_dotenv()

server_file_path = os.getenv("SERVER_FILE_PATH")
server_host = os.getenv("SERVER_HOST")
server_port = int(os.getenv("SERVER_PORT"))

file_path = os.getenv("SCREENSHOTS_DIRECTORY")

# logging.basicConfig(filename=f'{settings.log_dir}/error.log',
#                     level=logging.ERROR,
#                     format='%(asctime)s - %(levelname)s - %(message)s')


def handle_hotkey_press(username_global):
    keyboard.add_hotkey(hot_key, lambda: take_screenshot(username_global))


def take_screenshot(username_global):
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{username_global}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_directory, screenshot_name)
    pyautogui.screenshot(screenshot_path)
    send_file(screenshot_path)


def create_directories_if_not_exists(log_directory, scr_directory):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    if not os.path.exists(scr_directory):
        os.makedirs(scr_directory)


def send_file(file_path=settings.screenshots_directory):
    host, port = server_host, server_port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            with open(file_path, 'rb') as file:
                file_name = os.path.basename(file_path)
                print('FILE NAME: ', file_name)
                client_socket.sendall(file_name.encode())

                time.sleep(0.1)

                client_socket.sendall(file.read())
        return True

    except ConnectionRefusedError as e:
        logging.error(f"ConnectionRefusedError: {e}")
    except TimeoutError as e:
        logging.error(f"TimeoutError: {e}")
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
