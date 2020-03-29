from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QPushButton
from dataclasses import dataclass

from layouts.base import BaseLayout
from layouts.utils import get_elements
from controllers.controllers import init_experiment_table_plan

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


class ControllersLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_main_layout()

    def build_main_layout(self):
        layouts = get_elements(Layouts)
        buttons = get_elements(Buttons, [CREATE_TABLE_BUTTON_TEXT, START_CALCULATIONS_BUTTON_TEXT])

        self.connect_handlers(buttons)
        return self.makeup(layouts, buttons)

    @staticmethod
    def makeup(layouts, buttons):
        layouts.main_inner_layout.addWidget(buttons.create_table_button)
        layouts.main_inner_layout.addWidget(buttons.start_calculations_button)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    def connect_handlers(self, buttons):
        buttons.create_table_button.clicked.connect(
            lambda: init_experiment_table_plan(self.main_layout, self.experiment))