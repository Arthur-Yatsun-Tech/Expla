from typing import Tuple

from PySide2 import QtCore, QtWidgets, QtGui

 
def get_elements(dataclass, arguments=None):
    elements = {}
    for name, type_ in dataclass.__annotations__.items():
        try:
            argument = arguments.pop(0)
        except (AttributeError, IndexError):
            argument = None
        elements[name] = type_(argument)

    return dataclass(**elements)


def set_size(element: QtWidgets, size: Tuple[int, int]):
    """Set size to the element

    :param element: any widget or layout
    :param size: tuple of setting size (width, height)
    """
    element.setFixedSize(*size)


def set_style_sheet(element: QtWidgets, style_params: str):
    """

    :param element:
    :param style_params:
    """
    element.setStyleSheet(style_params)


def set_alignment(element: QtWidgets, alignment: QtCore.Qt):
    element.setAlignment(alignment)


def get_validator(expression: str):
    """"""
    return QtGui.QRegExpValidator(QtCore.QRegExp(expression))
