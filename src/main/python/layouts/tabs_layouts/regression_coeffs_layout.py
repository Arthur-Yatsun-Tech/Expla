from PySide2.QtWidgets import QTableWidget
from dataclasses import dataclass

from layouts import BaseLayout


@dataclass
class Table:
    table: QTableWidget


class RegressionCoeffsLayout(BaseLayout):
    """Table layout for the regression coefficients calculations"""

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        table = self.utils.get_elements(Table)

        return table

    def compose_layout(*args):
        pass