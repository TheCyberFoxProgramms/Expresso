import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidiget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidiget()
    ex.show()
    sys.exit(app.exec())