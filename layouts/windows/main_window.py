from PySide2.QtWidgets import QMainWindow

from layouts.main_layout import MainLayout


class MainWindow(QMainWindow):
    """Application main window class"""
    def __init__(self):
        super().__init__()
        self.showMaximized()

        widget = MainLayout().main_layout
        self.setCentralWidget(widget)
