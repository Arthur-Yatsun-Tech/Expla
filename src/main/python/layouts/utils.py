import collections
import random
from typing import Tuple

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QGroupBox, QLabel

from core.constants import VAR


class Utils:
    @staticmethod
    def get_elements(dataclass, arguments=None):
        elements = {}
        for name, type_ in dataclass.__annotations__.items():
            try:
                argument = arguments.pop(0)
            except (AttributeError, IndexError):
                argument = None
            elements[name] = type_(argument)

        return dataclass(**elements)

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
