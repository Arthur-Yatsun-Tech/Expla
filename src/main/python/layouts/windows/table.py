import PySide2.QtGui
from PySide2.QtWidgets import QMainWindow

from layouts.layouts_handlers.table_window.layouts import disable_parent, init_layouts
from layouts.layouts_handlers.table_window.elements.table import fill_random_numbers


class TableWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TableWindow, self).__init__(parent)

        disable_parent(parent)

        self.parent = parent
        self.factors = parent.factors
        self.experiments = parent.experiments
        self.levels = parent.levels
        self.columns = 100
        self.rows = self.factors * 25 if (self.levels == 5 and self.factors >= 5) \
            else self.levels ** self.factors

        widget = init_layouts(self)
        self.setCentralWidget(widget)

        # todo: remove it after the testing
        fill_random_numbers(self)

    # def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
    #     disable_parent(self.parent, mode=True)
    #     event.accept()
