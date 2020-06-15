import random

from PySide2.QtWidgets import QTableWidgetItem


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

