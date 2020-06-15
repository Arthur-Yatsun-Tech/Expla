from PySide2.QtWidgets import QMainWindow

from layouts.main_layout import MainLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.levels = 5
        self.factors = 0
        self.experiments = 0

        self.showMaximized()

        widget = MainLayout().main_layout
        self.setCentralWidget(widget)