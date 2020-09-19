from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
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

    rows_and_columns_for_title = ((0, 0), (0, 4), (0, 8))
    title_span_size = (1, 3)
    titles_names = (
        "Regression coefficients",
        "Optimized coefficients",
        "Bad coefficients"
    )

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        table = self.utils.get_elements(Table)
        self.utils.set_table_counts(table.table, ROWS, COLUMNS)
        self.utils.set_column_width(table.table, COLUMN_WIDTH, COLUMNS)
        self.set_titles(table.table)
        self.set_spans(table.table)
        return table.table

    def set_spans(self, table: QTableWidget):
        """Method to set table spans"""
        for row, column in self.rows_and_columns_for_title:
            self.utils.set_table_span(table, row, column, *self.title_span_size)

    def set_titles(self, table: QTableWidget):
        for coordinates, title in zip(self.rows_and_columns_for_title, self.titles_names):
            self.utils.set_table_item(table, *coordinates, title)


