from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QPushButton
from dataclasses import dataclass

from layouts import BaseLayout

CREATE_TABLE_BUTTON_TEXT = 'Создать таблицу эксперимента'
START_CALCULATIONS_BUTTON_TEXT = 'Произвести расчеты'


@dataclass
class Layouts:
    main_inner_layout: QVBoxLayout
    main_layout: QGroupBox


@dataclass
class Buttons:
    create_table_button: QPushButton
    start_calculations_button: QPushButton


class ManagingLayout(BaseLayout):
    """Layout for managing buttons"""
    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        buttons = self.utils.get_elements(
            Buttons, [CREATE_TABLE_BUTTON_TEXT, START_CALCULATIONS_BUTTON_TEXT])

        self.connect_handlers(buttons)
        return self.compose_layout(layouts, buttons)

    @staticmethod
    def compose_layout(layouts, buttons):
        layouts.main_inner_layout.addWidget(buttons.create_table_button)
        layouts.main_inner_layout.addWidget(buttons.start_calculations_button)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    def connect_handlers(self, buttons):
        buttons.create_table_button.clicked.connect(
            lambda: self.controllers.create_experiment_table_plan(self.main_layout))
        buttons.start_calculations_button.clicked.connect(
            lambda: self.controllers.calculate(self.main_layout))
