from functions import *
from keyboard_listener import start_key_listener
import tkinter as tk


login = start_app()
print('LOGIN: ', login)
if login:
    start_key_listener()
