from PyQt5.QtWidgets import QApplication

from qt_classes import LoginWindow

if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec_()