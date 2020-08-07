import collections
import random
from typing import Tuple, List
from string import ascii_uppercase

import openpyxl
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QGroupBox, QLabel
from dataclasses import dataclass

from core.constants import VAR
from core.experiment import Experiment
from core.table_planner import TablePlanner


class ControllersUtils:
    """Class to handle all elements controllers"""

    def __init__(self, experiment):
        self.experiment = experiment
        self.utils = Utils(experiment)

    def disable_experiments_cells_by_number_of_factors(self, parameters_layout: QGroupBox,
                                                       factors: int):
        """Method to disable cells in the experiments layout by the factor.
           Method is the controller of the QLineEdit for number of the factors

        :param parameters_layout: main parameters layout
        :param factors: number of the factors entered by the user
        """

        self.experiment.factors = self.utils.cast_parameter_to_int(factors)
        experiment_cells = self.utils.get_experiment_cells(parameters_layout)

        # todo: what is going on?
        x_cells = experiment_cells[:9][::-1]
        d1_cells = experiment_cells[9:18][::-1]
        d2_cells = experiment_cells[18:][::-1]

        if self.experiment.factors == 0:
            experiment_cells = list(set(experiment_cells) - set(d2_cells)) \
                if self.experiment.levels != 5 else experiment_cells
            list(map(
                lambda cell: self.utils.set_enabled(cell, True),
                experiment_cells))
        else:
            unused_cells = [
                *x_cells[:-self.experiment.factors],
                *d1_cells[:-self.experiment.factors],
                *d2_cells[:-self.experiment.factors]]
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                unused_cells))

    def disable_experiments_cells_by_variation_level(self,
                                                     variation_levels_layout: QGroupBox,
                                                     variation_level: int):
        """Method to disable cells in the experiments layout by the variation_level.
           Method is the controller of the QLineEdit for number of the factors

        :param variation_levels_layout: variation levels layout
        :param variation_level: variation level entered by the user
        """

        self.experiment.levels = self.utils.cast_parameter_to_int(variation_level)
        experiment_cells = self.utils.get_experiment_cells(variation_levels_layout)

        # todo: what is d2 cells?
        d2_cells = experiment_cells[18:]

        if self.experiment.levels != 5:
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                d2_cells))
        else:
            if self.experiment.factors == 9:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells))
            else:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells[:self.experiment.factors]))

    def set_number_of_experiments(self, experiment_series: int):
        """Method to set the number of experiments to the Experiment object.
           Method is the controller of the QLineEdit for the number of experiment series

        :param experiment_series: experiment series entered by the user
        """

        self.experiment.count_of_experiments = self.utils. \
            cast_parameter_to_int(experiment_series)

    def create_experiment_table_plan(self, controllers_layout: QGroupBox):
        """Method to create the experiment table plan

        :param controllers_layout: QGroupBox Object to get the table layout
            regarding its position
        """
        table = self.utils.get_experiment_table(controllers_layout)
        plan = TablePlanner(
            self.experiment.levels, self.experiment.factors).create_table()

        self.utils.set_experiment_plan(table, plan)

    def calculate(self, current_layout: QGroupBox):
        table = self.utils.get_experiment_table(current_layout)
        self.utils.get_experiments_data(table)

        statistics = self.experiment.calculate_statistics()
        self.utils.set_statistics(table, statistics)

        self.utils.set_criteria(current_layout, max(statistics['t']))


class Utils:

    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    @staticmethod
    def get_elements(class_: dataclass, arguments: List = None):
        """Method to create elements of dataclass with arguments or not

        :param class_: dataclass to create his elements
        :param arguments: arguments of the element of dataclass provided as list
        """

        elements = {}
        for name, type_ in class_.__annotations__.items():
            try:
                argument = arguments.pop(0)
            except (AttributeError, IndexError):
                argument = None
            elements[name] = type_(argument)
        return class_(**elements)

    @staticmethod
    def set_size(element: QtWidgets, size: Tuple[int, int]):
        """Set size to the element

        :param element: any widget or layout
        :param size: tuple of setting size (width, height)
        """
        element.setFixedSize(*size)

    @staticmethod
    def set_style_sheet(element: QtWidgets, style_params: str):
        """

        :param element:
        :param style_params:
        """
        element.setStyleSheet(style_params)

    @staticmethod
    def set_alignment(element: QtWidgets, alignment: QtCore.Qt):
        element.setAlignment(alignment)

    @staticmethod
    def get_validator(expression: str):
        """"""
        return QtGui.QRegExpValidator(QtCore.QRegExp(expression))

    @staticmethod
    def set_enabled(element, mode=False):
        element.setEnabled(mode)

    @staticmethod
    def cast_parameter_to_int(parameter):
        try:
            parameter = int(parameter)
        except ValueError:
            parameter = 0
        return parameter

    @staticmethod
    def get_experiment_cells(current_layout):
        main_window = current_layout.parent()
        return main_window.children()[3].findChildren(QLineEdit)

    @staticmethod
    def get_experiment_table(current_layout):
        main_window = current_layout.parent()
        tab_widget = main_window.children()[-1]
        return tab_widget.findChildren(QTableWidget)[-1]

    @staticmethod
    def get_regression_table(current_layout):
        main_window = current_layout.parent()
        tab_widget = main_window.children()[-1]
        return tab_widget.findChildren(QTableWidget)[0]

    def set_experiment_plan(self, table: QTableWidget, plan: collections.defaultdict):
        """Method to set the experiment plan into the table layout

        :param table: table widget
        :param plan: experiment plan
        """
        self.experiment.experiment_plan = plan

        for column, key in zip(range(self.experiment.factors), sorted(plan.keys())):
            for row in range(self.experiment.rows):
                table.setItem(row, column, QTableWidgetItem(
                    plan[key][row]))

        self.set_table_headers(table)
        # TODO: algorithm to set color
        # set_table_color(experiment, table)
        # TODO: remove this
        self.fill_random_numbers(table)

        if self.experiment.factors == 4 and \
                self.experiment.count_of_experiments == 2 and \
                self.experiment.levels == 2:
            filepath = "/home/arthur/expla/src/main/python/test_xlsx_files/chemicals.xlsx"
            self.read_and_paste_from_excel(table, filepath)

    def set_table_headers(self, table):
        x = [f'x{i + 1}' for i in range(self.experiment.factors)]
        y = [f'y{i + 1}' for i in range(self.experiment.count_of_experiments)]
        labels = x + y + VAR

        # TODO: add replace 100 on the COLUMNS variable
        [labels.append('') for _ in range(100 - len(labels))]

        table.setHorizontalHeaderLabels(labels)

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

    def get_experiments_data(self, table):
        for column in range(self.experiment.count_of_experiments):
            column_data = collections.deque()
            for row in range(self.experiment.rows):
                column_data.append(
                    float(table.item(row, column + self.experiment.factors).text()))
            self.experiment.experiments_data.append(column_data)

    def set_statistics(self, table, statistics):
        start_column = self.experiment.factors + self.experiment.count_of_experiments + 1
        for row in range(self.experiment.rows):
            table.setItem(row, start_column, QTableWidgetItem(
                str(statistics['mean'][row])))
            table.setItem(row, start_column + 1, QTableWidgetItem(
                str(statistics['variation'][row])))
            table.setItem(row, start_column + 2, QTableWidgetItem(
                str(statistics['std'][row])))
            table.setItem(row, start_column + 3, QTableWidgetItem(
                str(statistics['t'][row])))

    def set_criteria(self, current_layout, t_max):
        t_table = self.experiment.get_student_cirteria()

        main_window = current_layout.parent()
        tab_widget = main_window.children()[-1]
        critera_widget = tab_widget.findChildren(QGroupBox)[0]
        labels = critera_widget.findChildren(QLabel)

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

    @staticmethod
    def set_table_counts(table: QTableWidget, rows: int, columns: int):
        """Method to set the number of rows and columns in the table

        :param table: table to set the count
        :param rows: number of rows
        :param columns: number of columns
        """
        table.setRowCount(rows)
        table.setColumnCount(columns)

    @staticmethod
    def set_column_width(table: QTableWidget, width: int, columns: int):
        """Method to set the width of the columns in the table

        :param table: table widget to set column width
        :param width: width number
        :param columns: the count of the columns to set width
        """
        [table.setColumnWidth(i, width) for i in range(columns)]
