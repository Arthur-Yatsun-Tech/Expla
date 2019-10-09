import random

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableWidgetItem

from constants import COLORS


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


def get_experiments_data(experiments, number_of_rows, factors, table):
    y = []
    for column in range(experiments):
        column_data = []
        for row in range(number_of_rows):
            column_data.append(table.item(row, column + factors).text())

        y.append(column_data)
    return y


# переписать из-за того что словарь не упорядоченный
def set_table_signs(self):
    keys = list(self.plan.keys())
    for column in range(self.factors):
        for row in range(self.number_of_rows):
            self.table.setItem(row, column, QTableWidgetItem(self.plan[keys[column]][row]))

    set_table_color(self)


def set_table_color(self):
    if self.is_full_table:
        self.table.item(1, 1).setBackgroundColor(QColor(*COLORS[0]))
        self.table.item(1, 2).setBackgroundColor(QColor(*COLORS[1]))


def fill_random_numbers(self):
    for column in range(self.experiments):
        for row in range(self.number_of_rows):
            self.table.setItem(row, column + self.factors, QTableWidgetItem(str(random.randint(-100, 100))))


def fill_calculated_data(self):
    pass