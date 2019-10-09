import random
import sys

import PySide2
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem
from fbs_runtime.application_context.PySide2 import ApplicationContext
from pyside2uic.properties import QtGui

from table_planning.table_planer import TablePlanner
from controllers.table_window.table import disable_parent, get_experiments_data,    set_table_signs, fill_random_numbers
from controllers.table_window.buttons import calculate_data


class TableApp(QMainWindow):
    def __init__(self, parent=None):
        super(TableApp, self).__init__(parent)

        disable_parent(parent)

        self.parent = parent
        self.factors = parent.factors
        self.experiments = parent.experiments
        self.levels = parent.levels
        self.is_full_table = self.factors <= 6

        if self.is_full_table:
            self.number_of_rows = self.levels ** self.factors
        else:
            self.number_of_rows = self.factors * 25
        self.number_of_columns = 100

        self.table = QTableWidget()
        self.plan = TablePlanner(self.levels, self.factors).create_table()

        widget = QWidget()

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        calculate = QPushButton('Посчитать')
        continue_button = QPushButton('Продолжить')

        calculate.clicked.connect(lambda: calculate_data(self.table, self.y))

        button_layout.addWidget(save_button)
        button_layout.addWidget(calculate)
        button_layout.addWidget(continue_button)

        self.table.setRowCount(self.number_of_rows)
        self.table.setColumnCount(self.number_of_columns)

        headers = self._get_header_labels()
        self.table.setHorizontalHeaderLabels(headers)
        [self.table.setColumnWidth(i, 50) for i in range(self.number_of_columns)]

        self.showMaximized()

        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        set_table_signs(self)
        fill_random_numbers(self)
        self.y = get_experiments_data(self.experiments, self.number_of_rows, self.factors, self.table)
        print(self.y)

    def _get_header_labels(self):
        y_s = [f'y{i + 1}' for i in range(self.experiments)]
        headers = list(self.plan.keys()) + y_s
        return headers

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        disable_parent(self.parent, mode=True)
        event.accept()


if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = TableApp()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
