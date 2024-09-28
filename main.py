import sys
from PyQt6.QtWidgets import QApplication
from gui import MainMenu


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MainMenu()
    myApp.showMaximized()
    sys.exit(app.exec())
    