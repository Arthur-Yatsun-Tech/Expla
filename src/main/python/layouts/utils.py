import collections
import random
from typing import Tuple, List

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QGroupBox, QLabel
from dataclasses import dataclass

from core.constants import VAR
from core.table_planner import TablePlanner


class ControllersUtils:
    """Class to handle all elements controllers"""

    def __init__(self):
        self.utils = Utils()

    def disable_experiments_cells_by_number_of_factors(self, parameters_layout: QGroupBox,
                                                       experiment: "Experiment",
                                                       factors: int):
        """Method to disable cells in the experiments layout by the factor.
           Method is the controller of the QLineEdit for number of the factors

        :param parameters_layout: main parameters layout
        :param experiment: Experiment object to write in the experiment factors
        :param factors: number of the factors entered by the user
        """

        experiment.factors = self.utils.cast_parameter_to_int(factors)
        experiment_cells = self.utils.get_experiment_cells(parameters_layout)

        # todo: what is going on?
        x_cells = experiment_cells[:9][::-1]
        d1_cells = experiment_cells[9:18][::-1]
        d2_cells = experiment_cells[18:][::-1]

        if experiment.factors == 0:

            experiment_cells = list(set(experiment_cells) - set(d2_cells)) if experiment.levels != 5 else \
                               experiment_cells
            list(map(
                lambda cell: self.utils.set_enabled(cell, True),
                experiment_cells))
        else:
            unused_cells = [
                *x_cells[:-experiment.factors],
                *d1_cells[:-experiment.factors],
                *d2_cells[:-experiment.factors]]
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                unused_cells))

    def disable_experiments_cells_by_variation_level(self,
                                                     variation_levels_layout: QGroupBox,
                                                     experiment: "Experiment",
                                                     variation_level: int):
        """Method to disable cells in the experiments layout by the variation_level.
           Method is the controller of the QLineEdit for number of the factors

        :param variation_levels_layout: variation levels layout
        :param experiment: Experiment object
        :param variation_level: variation level entered by the user
        """

        experiment.levels = self.utils.cast_parameter_to_int(variation_level)
        experiment_cells = self.utils.get_experiment_cells(variation_levels_layout)

        # todo: what is d2 cells?
        d2_cells = experiment_cells[18:]

        if experiment.levels != 5:
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                d2_cells))
        else:
            if experiment.factors == 9:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells))
            else:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells[:experiment.factors]))

    def set_number_of_experiments(self, experiment: "Experiment", experiment_series: int):
        """Method to set the number of experiments to the Experiment object.
           Method is the controller of the QLineEdit for the number of experiment series

        :param experiment: experiment object to set the experiment_series entered by user
        :param experiment_series: experiment series entered by the user
        """

        experiment.count_of_experiments = self.utils. \
            cast_parameter_to_int(experiment_series)

    def create_experiment_table_plan(self, controllers_layout: "QGroupBox",
                                     experiment: "Experiment"):
        """Method to create the experiment table plan"""

        # todo: simplify this
        table = self.utils.get_experiment_table(controllers_layout)

        plan = TablePlanner(experiment.levels, experiment.factors).create_table()
        self.utils.set_experiment_plan(experiment, table, plan)

    def calculate(self, current_layout, experiment):
        table = self.utils.get_experiment_table(current_layout)
        self.utils.get_experiments_data(experiment, table)

        statistics = experiment.calculate_statistics()
        self.utils.set_statistics(table, experiment, statistics)

        self.utils.set_criteria(current_layout, experiment, max(statistics['t']))


class Utils:
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
        return tab_widget.findChild(QTableWidget)

    def set_experiment_plan(self, experiment, table, plan):
        for column, key in zip(range(experiment.factors), plan.keys()):
            for row in range(experiment.rows):
                table.setItem(row, column, QTableWidgetItem(
                    plan[key][row]))

        self.set_table_headers(experiment, table)
        # TODO: algorithm to set color
        # set_table_color(experiment, table)
        # TODO: remove this
        self.fill_random_numbers(experiment, table)

    @staticmethod
    def set_table_headers(experiment, table):
        x = [f'x{i + 1}' for i in range(experiment.factors)]
        y = [f'y{i + 1}' for i in range(experiment.count_of_experiments)]
        labels = x + y + VAR

        # TODO: add replace 100 on the COLUMNS variable
        [labels.append('') for _ in range(100 - len(labels))]

        table.setHorizontalHeaderLabels(labels)

    @staticmethod
    def fill_random_numbers(experiment, table):
        for column in range(experiment.count_of_experiments):
            for row in range(experiment.rows):
                table.setItem(row, column + experiment.factors,
                              QTableWidgetItem(str(random.randint(-100, 100))))

    @staticmethod
    def get_experiments_data(experiment, table):
        for column in range(experiment.count_of_experiments):
            column_data = collections.deque()
            for row in range(experiment.rows):
                column_data.append(
                    float(table.item(row, column + experiment.factors).text()))
            experiment.experiments_data.append(column_data)

    @staticmethod
    def set_statistics(table, experiment, statistics):
        start_column = experiment.factors + experiment.count_of_experiments + 1
        for row in range(experiment.rows):
            table.setItem(row, start_column, QTableWidgetItem(
                str(statistics['mean'][row])))
            table.setItem(row, start_column + 1, QTableWidgetItem(
                str(statistics['variation'][row])))
            table.setItem(row, start_column + 2, QTableWidgetItem(
                str(statistics['std'][row])))
            table.setItem(row, start_column + 3, QTableWidgetItem(
                str(statistics['t'][row])))

    @staticmethod
    def set_criteria(current_layout, experiment, t_max):
        t_table = experiment.get_student_cirteria()

        main_window = current_layout.parent()
        tab_widget = main_window.children()[-1]
        critera_widget = tab_widget.findChildren(QGroupBox)[0]
        labels = critera_widget.findChildren(QLabel)

        student_result_label = labels[1]
        fisher_result_label = labels[2]

        result = 'соблюдается' if t_max < t_table else \
            'не соблюдается'

        student_result_label.setText(
            f't-табличное (α=0.05, df={experiment.count_of_experiments - 1}):\n'
            f'{t_table}\n'
            f'Максимальное расчетное значение:\n'
            f'{t_max}\n\n'
            f'Условие t-расчетное < t-табличное {result}')
