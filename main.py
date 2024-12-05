import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class CoffeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.change_btn.clicked.connect(self.open_edit)
        self.modified = {}
        self.titles = None
        # self.id_change = []
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute('select * from coffees').fetchall()
        self.table_coffee.setRowCount(len(result))
        self.table_coffee.setColumnCount(8)
        self.table_coffee.setHorizontalHeaderLabels([description[0] for description in cur.description])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table_coffee.setItem(i, j, QTableWidgetItem(str(val)))

    def open_edit(self):
        self.coffee_edit = ChangeWindow(self)
        self.coffee_edit.show()


class ChangeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.load_btn.clicked.connect(self.load_res)
        self.table_coffee_id.itemChanged.connect(self.item_changed)
        self.save_btn.clicked.connect(self.save_results)
        self.price.setRange(0, 1000)
        self.volume.setRange(0, 1000)
        self.modified = {}
        self.titles = None
        self.add_btn.clicked.connect(self.add_coffee)

    def load_res(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffees WHERE id=?",
                             (item_id := self.id_box.text(),)).fetchall()
        self.table_coffee_id.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.table_coffee_id.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table_coffee_id.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = f"{item.text()}"

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffees SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += " WHERE id = ?"
            cur.execute(que, (int(self.id_box.text()),))
            self.con.commit()
            self.modified.clear()
            self.parent.update_result()

    def add_coffee(self):
        if self.title_coffee.text():
            self.statusBar().showMessage('')
            cur = self.con.cursor()
            que = '''insert into coffees (title_coffee, title_sorts, roast_degree, status, taste, price, volume)
            values (?, ?, ?, ?, ?, ?, ?)'''
            cur.execute(que, (self.title_coffee.text(), self.title_sorts.text(), self.roast_degree.text(),
                              self.status.currentText(), self.taste.text(),
                              int(self.price.value()), int(self.volume.value())))
            self.con.commit()
            self.parent.update_result()
        else:
            self.statusBar().showMessage('Вы обязаны ввести хотя бы название')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeMainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())