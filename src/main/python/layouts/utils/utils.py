import collections
import random
from string import ascii_uppercase

import openpyxl
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QGroupBox, QLabel

from core.constants import VAR
from core.experiment import Experiment


class Utils:
    """Base utils class"""

    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    def set_experiment_plan(self, table: QTableWidget, plan: collections.defaultdict):
        """Method to set the experiment plan into the table layout

        :param table: table widget
        :param plan: experiment plan
        """
        self.experiment.set_experiments_plan(plan)

        for column, key in zip(range(self.experiment.factors), sorted(plan.keys())):
            for row in range(self.experiment.rows):
                table.setItem(row, column, QTableWidgetItem(
                    plan[key][row]))

        self.set_experiment_table_headers(table)
        # TODO: algorithm to set color
        # set_table_color(experiment, table)
        # TODO: remove this after tests
        self.fill_random_numbers(table)

        if self.experiment.factors == 4 and \
                self.experiment.count_of_experiments == 2 and \
                self.experiment.levels == 2:
            filepath = "/home/arthur/expla/src/main/python/test_xlsx_files/chemicals.xlsx"
            self.read_and_paste_from_excel(table, filepath)

        if self.experiment.factors == 4 and \
                self.experiment.count_of_experiments == 3 and \
                self.experiment.levels == 2:
            filepath = "/home/arthur/expla/src/main/python/test_xlsx_files/exp_data.xlsx"
            self.read_and_paste_from_excel(table, filepath)

    def set_statistics_data(self, table):
        """Method to set statistics data into the experiment table

        :param table: experiment table
        """
        start_column = self.experiment.factors + self.experiment.count_of_experiments + 1
        for row in range(self.experiment.rows):
            table.setItem(row, start_column, QTableWidgetItem(
                str(self.experiment.mean[row])))
            table.setItem(row, start_column + 1, QTableWidgetItem(
                str(self.experiment.variation[row])))
            table.setItem(row, start_column + 2, QTableWidgetItem(
                str(self.experiment.std[row])))
            table.setItem(row, start_column + 3, QTableWidgetItem(
                str(self.experiment.student_criteria[row])))

    def set_criteria(self, current_layout, t_max):
        """Method to set the criteria results in the criteria labels"""
        t_table = self.experiment.calculator.get_student_table_value(
            self.experiment.count_of_experiments - 1)
        main_window = current_layout.parent()
        tab_widget = main_window.children()[-1]
        criteria_widget = tab_widget.findChildren(QGroupBox)[0]
        labels = criteria_widget.findChildren(QLabel)

        student_result_label = labels[1]
        fisher_result_label = labels[2]

        result = 'соблюдается' if t_max < t_table else \
            'не соблюдается'

        student_result_label.setText(
            f't-табличное (α=0.05, df={self.experiment.count_of_experiments - 1}):\n'
            f'{t_table}\n'
            f'Максимальное расчетное значение:\n'
            f'{t_max}\n\n'
            f'Условие t-расчетное < t-табличное {result}')

    def set_regression_coeffs(self, regression_table: QTableWidget):
        """Method to set the regression coefficients

        :param regression_table: regression table to set the coeffs
        """
        coeffs_names = sorted(
            map(lambda x: int(x), self.experiment.regression_coeffs.keys()))
        coeffs = self.experiment.regression_coeffs

        for row, name in zip(range(self.experiment.rows), coeffs_names):
            regression_table.setItem(row, 0, QTableWidgetItem(
                'b' + str(name)))
            regression_table.setItem(row, 1, QTableWidgetItem(
                str(coeffs[str(name)])))

    def set_experiment_table_headers(self, table):
        x = [f'x{i + 1}' for i in range(self.experiment.factors)]
        y = [f'y{i + 1}' for i in range(self.experiment.count_of_experiments)]
        labels = x + y + VAR

        # TODO: add replace 100 on the COLUMNS variable
        [labels.append('') for _ in range(100 - len(labels))]

        table.setHorizontalHeaderLabels(labels)

    def get_experiments_data(self, table: QTableWidget):
        """Method to get the experiments data and set it to the Experiment object

        :param table: experiment table widget
        """
        experiments_data = []
        for column in range(self.experiment.count_of_experiments):
            column_data = collections.deque()
            for row in range(self.experiment.rows):
                column_data.append(
                    float(table.item(row, column + self.experiment.factors).text()))
            experiments_data.append(column_data)
        self.experiment.set_experiments_data(experiments_data)

    def fill_random_numbers(self, table):
        for column in range(self.experiment.count_of_experiments):
            for row in range(self.experiment.rows):
                table.setItem(row, column + self.experiment.factors,
                              QTableWidgetItem(str(random.randint(-100, 100))))

    def read_and_paste_from_excel(self, table: QTableWidget, filepath: str):
        book = openpyxl.load_workbook(filepath)
        sheet = book.active

        # indexes of the columns in excel are in the format A1, B1, C1.. AA1, AB1..
        # here we get the last index of the column regarding the count of experiments
        # TODO: add AA1.. indexes
        end_letter_index = ascii_uppercase[self.experiment.count_of_experiments-1:][0]
        cells = sheet["A1": f"{end_letter_index}{self.experiment.rows}"]

        # get the values of the cells from the Cell object in format
        # [[row1value1, row1value2..], [row2value1, row2value2..].. ]
        # to format
        # [[column1value1, column1value2..], [column2value1, column2value2].. ]
        cells = list(zip(*map(lambda x: [value.value for value in x], cells)))

        for column in range(self.experiment.count_of_experiments):
            for row in range(self.experiment.rows):
                table.setItem(row, column + self.experiment.factors,
                              QTableWidgetItem(str(cells[column][row])))


