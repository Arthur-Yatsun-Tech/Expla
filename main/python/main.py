import sys

from PySide2.QtWidgets import (QMainWindow, QGridLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout,
                               QRadioButton, QHBoxLayout, QWidget,
                               QPushButton)
from fbs_runtime.application_context.PySide2 import ApplicationContext

from controllers.main_window.groups import Groups
from controllers.main_window.buttons import planning_table
from controllers.main_window.qlines import set_factors, set_experiments
from controllers.main_window.radios import set_level


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.levels = 3
        self.factors = 3
        self.experiments = 4

        group = Groups(self)
        widget = QWidget()

        # ------------------------------- top left
        self.top_left_group = QGroupBox()

        self.number_of_factors = QLineEdit()
        self.number_of_experiments = QLineEdit()

        self.number_of_factors.textEdited.connect(lambda: set_factors(self))
        self.number_of_experiments.textEdited.connect(lambda: set_experiments(self))

        # -------------------------------- top right
        self.top_right_group = QGroupBox()

        self.level_5 = QRadioButton('5')
        self.level_3 = QRadioButton('3')
        self.level_2 = QRadioButton('2')

        self.level_5.clicked.connect(lambda: set_level(self, self.level_5.text()))
        self.level_3.clicked.connect(lambda: set_level(self, self.level_3.text()))
        self.level_2.clicked.connect(lambda: set_level(self, self.level_2.text()))

        # --------------------------------- bottom left
        self.bottom_left_group = QGroupBox()
        self.bottom_left_layout = QHBoxLayout()

        self.columns = [QVBoxLayout() for _ in range(10)]
        self.rows_edit_x = [QLineEdit() for _ in range(9)]
        self.rows_edit_d1 = [QLineEdit() for _ in range(9)]
        self.rows_edit_d2 = [QLineEdit() for _ in range(9)]

        # --------------------------------- bottom right
        self.bottom_right_group = QGroupBox()

        self.export_table_button = QPushButton('Сохранить таблицу')
        self.import_table_button = QPushButton('Загрузить таблицу')
        self.open_table_button = QPushButton('Открыть таблицу эксперимента')

        self.open_table_button.clicked.connect(lambda: planning_table(self))

        # =================================
        group.create_top_left_group_box()
        group.create_top_right_group_box()
        group.create_bottom_left_group_box()
        group.create_bottom_right_group_box()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.top_left_group, 1, 0)
        self.main_layout.addWidget(self.top_right_group, 1, 1)
        self.main_layout.addWidget(self.bottom_left_group, 2, 0)
        self.main_layout.addWidget(self.bottom_right_group, 2, 1)

        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    @staticmethod
    def _add_widgets_into_column(column, label_text, edit_x, edit_d1, edit_d2=None):
        column.addWidget(QLabel(label_text))
        column.addWidget(edit_x)
        column.addWidget(edit_d1)
        if edit_d2 is not None:
            column.addWidget(edit_d2)


if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = MainApp()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
