from table_planning.table_preparer import TablePreparer
from table import TableApp


def save_table(self):
    print('save table')


def planning_table(self):
    table = TableApp(self)
    table.show()
