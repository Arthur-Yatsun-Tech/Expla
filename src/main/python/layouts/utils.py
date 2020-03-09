from typing import Tuple

import PySide2
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout


def set_size(element: PySide2.QtWidgets, size: Tuple[int, int]):
    """Set size to the element

    :param element: any widget or layout
    :param size: tuple of setting size (width, height)
    """
    element.setFixedSize(*size)


def set_style_sheet(element: PySide2.QtWidgets, style_params: str):
    """

    :param element:
    :param style_params:
    """
    element.setStyleSheet(style_params)


def get_qlabel(text: str = None):
    """Create QLabel"""
    return QLabel(text)


def get_qline():
    """Create QLineEdit"""
    return QLineEdit()


def get_hbox():
    return QHBoxLayout()


def get_vbox():
    return QVBoxLayout()


def get_validator(expression: str):
    """"""
    return QRegExpValidator(QRegExp(expression))
