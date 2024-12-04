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
        # self.pushButton.clicked.connect(self.update_result)
        # self.table_coffee.itemChanged.connect(self.item_changed)
        # self.pushButton_2.clicked.connect(self.save_results)
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

        self.modified = {}

    # def item_changed(self, item):
    #     self.modified[self.titles[item.column()]] = item.text()
    #
    # def save_results(self):
    #     if self.modified:
    #         cur = self.con.cursor()
    #         que = "UPDATE films SET\n"
    #         que += ", ".join([f"{key}='{self.modified.get(key)}'"
    #                           for key in self.modified.keys()])
    #         que += "WHERE id = ?"
    #         print(que)
    #         cur.execute(que, (self.spinBox.text(),))
    #         self.con.commit()
    #         self.modified.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeMainWindow()
    ex.show()
    sys.exit(app.exec())