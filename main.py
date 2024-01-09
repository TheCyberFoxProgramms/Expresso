import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidiget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run_btn)

    def run_btn(self):
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = list(cur.execute('''SELECT
                                        id,
                                        sort,
                                        roasting.roasting,
                                        types.type,
                                        description,
                                        price,
                                        volume
                                     FROM
                                       coffee
                                     INNER JOIN types
                                        ON types.id = coffee.type
                                     INNER JOIN roasting
                                          ON roasting.id = coffee.roasting''').fetchall())
        print(res)
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