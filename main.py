import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


# tableWidget

class MyWidiget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run_btn)

    def run_btn(self):
        def dop_connect(data):
            per1 = next(cur.execute(f'''SELECT type FROM types WHERE id == '{data[3]}' '''))
            per2 = next(cur.execute(f'''SELECT roasting FROM roasting WHERE id == '{data[3]}' '''))
            data = list(data)
            data[3] = per1[0]
            data[2] = per2[0]
            return tuple(data)

        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                 'объем упаковки']
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = list(map(dop_connect, cur.execute('''SELECT * FROM coffee''').fetchall()))
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(res))
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidiget()
    ex.show()
    sys.exit(app.exec())
