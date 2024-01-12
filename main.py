import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton


# tableWidget

class MyWidiget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run_btn)
        self.pushButton_2.clicked.connect(self.new_form)

    def new_form(self):
        self.new_window = NewForm()
        self.new_window.show()

    def run_btn(self):
        def dop_connect(data):
            per1 = next(cur.execute(f'''SELECT type FROM types WHERE id == '{data[3]}' '''))
            per2 = next(cur.execute(f'''SELECT roasting FROM roasting WHERE id == '{data[2]}' '''))
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


class NewForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton11.clicked.connect(self.get_result)
        self.pushButton12.clicked.connect(self.save_results)
        self.pushButton_zap.clicked.connect(self.append_new_res)
        self.modified = list()
        self.check = None

    def get_result(self):
        self.statusBar().showMessage('Запрос выполнен!')
        self.modified.clear()
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id := self.lineEdit_id.text(),)).fetchall()
        self.tableWidget11.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget11.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget11.setHorizontalHeaderLabels(self.titles)
        self.check = list(result[0])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.modified.append(val)
                self.tableWidget11.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget11.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        if item.text().isdigit():
            self.modified[item.column()] = int(item.text())
        else:
            self.modified[item.column()] = item.text()
        if len(self.modified) == len(self.check):
            if self.check[0] != self.modified[0]:
                self.statusBar().showMessage('Изменять ID запрещено! ID не будет изменен!')
                self.modified.clear()
                self.modified = [i for i in self.check]

    def save_results(self):
        const_id = {0: 'id', 1: 'sort', 2: 'roasting', 3: 'type', 4: 'description', 5: 'price', 6: 'volume'}
        if self.modified != self.check:
            cur = self.con.cursor()
            for ind, val in enumerate(self.modified):
                if val != self.check[ind]:
                    cur.execute(f''' UPDATE Coffee
                                      SET {const_id[ind]} = '{val}'
                                      WHERE id = '{self.check[0]}' ''')
            self.con.commit()

    def append_new_res(self):
        self.statusBar().showMessage('')
        cur = self.con.cursor()
        old_id = list(cur.execute(''' SELECT id FROM Coffee ''').fetchall())[-1][0] + 1
        new_data = self.lineEdit_zap.text().split()
        new_data.insert(0, old_id)
        type = {k: v for v, k in cur.execute(''' SELECT * FROM types ''').fetchall()}
        roas = {k: v for v, k in cur.execute(''' SELECT * FROM roasting ''').fetchall()}
        if len(new_data) == 7:
            if new_data[2] in roas:
                if new_data[3] in type:
                    if new_data[5].isdigit() and new_data[6].isdigit():
                        new_data[2] = roas[new_data[2]]
                        new_data[3] = type[new_data[3]]
                        new_data[5] = int(new_data[5])
                        new_data[6] = int(new_data[6])
                        cur.execute(f''' INSERT INTO Coffee (id, sort, roasting, type, description, price,
                        volume) VALUES{str(tuple(new_data))} ''')
                        self.con.commit()
                        self.statusBar().showMessage(f'Новое значение добавлено в базу данных')
                    else:
                        self.statusBar().showMessage(f'Не верные данные! Пятое и шестое значения, должны быть числом')
                else:
                    self.statusBar().showMessage(
                        f'Не верные данные! Третье значение должно иметь вид: {" или ".join(type)}')
            else:
                self.statusBar().showMessage(
                    f'Не верные данные! Второе значение должно иметь вид: {" или ".join(roas)}')
        else:
            self.statusBar().showMessage('Ошибка! кол-во данных должно ровняться 6')

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidiget()
    ex.show()
    sys.exit(app.exec())
