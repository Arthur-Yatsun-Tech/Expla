import sys

from PySide2.QtWidgets import QMainWindow
from fbs_runtime.application_context.PySide2 import ApplicationContext

import controllers.main_window.layouts as layouts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.levels = 5
        self.factors = 0
        self.experiments = 0

        self.showMaximized()

        widget = layouts.init_layouts(self)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    expla = ApplicationContext()
    window = MainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = expla.app.exec_()
    sys.exit(exit_code)
