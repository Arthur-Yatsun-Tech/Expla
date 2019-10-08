import random
import sys

import PySide2
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem
from fbs_runtime.application_context.PySide2 import ApplicationContext
import numpy as np

from table_planning.table_planer import TablePlanner


class TableApp(QMainWindow):
    def __init__(self, parent=None):
        super(TableApp, self).__init__(parent)

        self.parent = parent

        self.disable_parent(parent)

        self.factors = parent.factors
        self.experiments = parent.experiments
        self.levels = parent.levels
        self.number_of_columns = self.factors + self.experiments

        if self.factors <= 5:
            self.number_of_rows = self.levels ** self.factors
        else:
            self.number_of_rows = self.factors * 25

        widget = QWidget()
        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        continue_button = QPushButton('Продолжить')
        button_layout.addWidget(save_button)
        button_layout.addWidget(continue_button)

        self.plan = TablePlanner(self.levels, self.factors).create_table()
        self.table = QTableWidget()
        self.table.setRowCount(self.number_of_rows)
        self.table.setColumnCount(self.number_of_columns)
        self.headers = self._get_header_labels()
        self.table.setHorizontalHeaderLabels(self.headers)
        [self.table.setColumnWidth(i, 50) for i in range(self.number_of_columns)]

        self._set_table_signs()
        self._fill_random_numbers()

        self.table.resizeColumnsToContents()

        self._get__experiments_data()

        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _get_header_labels(self):
        y_s = [f'y{i + 1}' for i in range(self.experiments)]
        headers = list(self.plan.keys()) + y_s
        return headers

    # переписать из-за того что словарь не упорядоченный
    def _set_table_signs(self):
        keys = list(self.plan.keys())
        for column in range(self.factors):
            for row in range(self.number_of_rows):
                self.table.setItem(row, column, QTableWidgetItem(self.plan[keys[column]][row]))

    def _fill_random_numbers(self):
        for column in range(self.experiments):
            for row in range(self.number_of_rows):
                self.table.setItem(row, column + self.factors, QTableWidgetItem(str(random.randint(-100, 100))))

    @staticmethod
    def disable_parent(parent, mode=False):
        parent.number_of_experiments.setEnabled(mode)
        parent.number_of_factors.setEnabled(mode)
        parent.level_5.setEnabled(mode)
        parent.level_3.setEnabled(mode)
        parent.level_2.setEnabled(mode)
        [column.setEnabled(mode) for column in parent.rows_edit_x]
        [column.setEnabled(mode) for column in parent.rows_edit_d1]
        [column.setEnabled(mode) for column in parent.rows_edit_d2]
        parent.export_table_button.setEnabled(mode)
        parent.import_table_button.setEnabled(mode)
        parent.open_table_button.setEnabled(mode)

    def _get__experiments_data(self):
        self.y = []
        for column in range(self.experiments):
            column_data = []
            for row in range(self.number_of_rows):
                column_data.append(self.table.item(row, column + self.factors).text())

            self.y.append(column_data)

    def _count_mean(self):
        self.table.setHorizontalHeaderLabels(self.headers)


    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        self.disable_parent(self.parent, mode=True)
        event.accept()


if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = TableApp()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
