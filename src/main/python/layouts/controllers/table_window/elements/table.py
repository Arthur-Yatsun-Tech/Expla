import random

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableWidgetItem

from core.constants import COLORS, CURRENT_PARAMETER_COLOR


def get_experiments_data(experiments, number_of_rows, factors, table):
    y = []
    for column in range(experiments):
        column_data = []
        for row in range(number_of_rows):
            column_data.append(table.item(row, column + factors).text())

        y.append(column_data)
    return y


def set_plan(table, plan, factors, rows, levels):
    keys = [f'x{i + 1}' for i in range(factors)]
    for column in range(factors):
        for row in range(rows):
            table.setItem(row, column, QTableWidgetItem(plan[keys[column]][row]))

    set_table_color(table, factors, rows, levels)


def fill_random_numbers(self):
    for column in range(self.experiments):
        for row in range(self.rows):
            self.table.setItem(row, column + self.factors, QTableWidgetItem(str(random.randint(-100, 100))))


def fill_calculated_data(self):
    start_point = self.experiments + self.factors + 1

    for row in range(self.rows):
        self.table.setItem(row, start_point, QTableWidgetItem(str(self.mean[row])))
        self.table.setItem(row, start_point + 1, QTableWidgetItem(str(self.var[row])))
        self.table.setItem(row, start_point + 2, QTableWidgetItem(str(self.std[row])))


def set_table_color(table, factors, rows, levels):
    if not (levels == 5 and factors >= 5):
        for columns in range(factors, 0, -1):
            print(f'columns {columns}')
            for column in range(columns):
                if columns == 1:
                    break
                for row in range(levels ** columns):
                    table.item(row, column).setBackgroundColor(QColor(*COLORS[columns]))
    else:
        for columns in range(factors, 0, -1):

            for column in range(factors):
                for row in range(25 * columns - 25, 25 * columns):
                    table.item(row, column).setBackgroundColor(QColor(*COLORS[columns]))

            for row in range(25 * columns - 25, 25 * columns):
                table.item(row, columns - 1).setBackgroundColor(QColor(*CURRENT_PARAMETER_COLOR))

