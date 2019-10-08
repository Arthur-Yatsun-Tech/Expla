from numpy import NaN

from .table_planer import TablePlanner


class TablePreparer:
    def __init__(self, level, x_count, y_count):
        self.table = TablePlanner(level, x_count).create_table()
        self.table = self._prepare(y_count, self.table)

    @staticmethod
    def _prepare(y_count, table):
        for i in range(y_count):
            table[f'y{i + 1}'] = NaN
        return table


if __name__ == '__main__':
    preparer = TablePreparer(2, 4, 2)
    print(preparer.table)