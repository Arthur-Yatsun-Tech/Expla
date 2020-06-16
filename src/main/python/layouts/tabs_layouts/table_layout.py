from PySide2.QtWidgets import QTableWidget
from dataclasses import dataclass

from layouts.base import BaseLayout

ROWS = 1000
COLUMNS = 100

COLUMN_WIDTH = 50


@dataclass
class Table:
    table: QTableWidget


class TableLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_main_layout()

    def build_main_layout(self):
        table = self.utils.get_elements(Table)
        self.set_table_counts(table.table, ROWS, COLUMNS)
        self.set_column_width(table.table, COLUMN_WIDTH, COLUMNS)

        return table.table

    @staticmethod
    def set_table_counts(table, rows, columns):
        table.setRowCount(rows)
        table.setColumnCount(columns)

    @staticmethod
    def set_column_width(table, width, columns):
        [table.setColumnWidth(i, width) for i in range(columns)]

