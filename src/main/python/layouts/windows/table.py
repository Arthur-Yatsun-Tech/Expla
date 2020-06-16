from layouts.tabs_layouts.table_layout import TableLayout

from PySide2.QtWidgets import QMainWindow


class TableWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TableWindow, self).__init__(parent)

        self.parent = parent
        self.factors = parent.factors
        self.experiments = parent.experiments
        self.levels = parent.levels
        self.columns = 100
        self.rows = self.factors * 25 if (self.levels == 5 and self.factors >= 5) \
            else self.levels ** self.factors

        widget = TableLayout().main_layout
        self.setCentralWidget(widget)
