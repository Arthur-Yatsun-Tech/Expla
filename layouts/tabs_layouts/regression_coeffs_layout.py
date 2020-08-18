from PySide2.QtWidgets import QTableWidget
from dataclasses import dataclass

from layouts import BaseLayout

ROWS = 100
COLUMNS = 40

COLUMN_WIDTH = 60


@dataclass
class Table:
    table: QTableWidget


class RegressionCoeffsLayout(BaseLayout):
    """Table layout for the regression coefficients calculations"""

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        table = self.utils.get_elements(Table)
        self.utils.set_table_counts(table.table, ROWS, COLUMNS)
        self.utils.set_column_width(table.table, COLUMN_WIDTH, COLUMNS)
        return table.table
