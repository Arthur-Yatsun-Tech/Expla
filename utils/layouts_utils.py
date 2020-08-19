from typing import List, Tuple

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QLineEdit, QTableWidget
from dataclasses import dataclass

from core.experiment import Experiment
from utils.utils import Utils


class LayoutsUtils(Utils):
    """Utils class for layouts needs"""
    def __init__(self, experiment: Experiment):
        super().__init__(experiment)

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
        element.setStyleSheet(style_params)

    @staticmethod
    def set_alignment(element: QtWidgets, alignment: QtCore.Qt):
        element.setAlignment(alignment)

    @staticmethod
    def get_validator(expression: str):
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