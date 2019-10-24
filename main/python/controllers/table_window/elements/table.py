import random

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableWidgetItem

from constants import COLORS


def get_experiments_data(experiments, number_of_rows, factors, table):
    y = []
    for column in range(experiments):
        column_data = []
        for row in range(number_of_rows):
            column_data.append(table.item(row, column + factors).text())

        y.append(column_data)
    return y


def set_plan(table, plan, factors, rows):
    keys = [f'x{i + 1}' for i in range(factors)]
    print(plan)
    for column in range(factors):
        for row in range(rows):
            table.setItem(row, column, QTableWidgetItem(plan[keys[column]][row]))

    # set_table_color(self)


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

# def set_table_color(self):
#     def get_blocks(column):
#         if column == 0 or column == 1:
#             return self.factors - 1
#         else:
#             return self.factors - column
#
#     if self.is_not_full_table:
#         for column in range(self.factors):
#             block_size = self.levels ** (column + 1)
#             colors = COLORS
#
#             if column == 0:
#                 block_size = self.levels ** (column + 2)
#
#             print(f'block size {block_size}')
#             print(get_blocks(column))
#
#             for block in range(get_blocks(column)):
#                 for row in range(self.levels ** (block + 1), self.levels ** (block + 2)):
#
#                     self.table.item(row - self.levels, column).setBackgroundColor(QColor(*colors[block]))
#
#                     # if column == 0:
#                     #     self.table.item(row, column).setBackgroundColor(QColor(*colors[-block]))
#                     # else:
#                     #     self.table.item(row, column).setBackgroundColor(QColor(*colors[-block]))
#                     #     colors.pop()
