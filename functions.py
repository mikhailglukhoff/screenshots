import datetime
import os

import keyboard
import pyautogui

from settings import hot_key, screenshots_directory


def handle_hotkey_press(username_global):
    keyboard.add_hotkey(hot_key, lambda: take_screenshot(username_global))


def take_screenshot(username_global):
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{username_global}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_directory, screenshot_name)
    pyautogui.screenshot(screenshot_path)
