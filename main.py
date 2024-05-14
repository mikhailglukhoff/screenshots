import settings
import logging

from PyQt5.QtWidgets import QApplication
from qt_classes import LoginWindow
from functions import create_directories_if_not_exists

create_directories_if_not_exists(f'{settings.log_dir}', f'{settings.screenshots_directory}')

logging.basicConfig(filename=f'{settings.log_dir}/error.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec_()
