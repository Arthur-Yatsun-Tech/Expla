from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QPushButton
from dataclasses import dataclass

from layouts.utils import get_elements

CREATE_TABLE_BUTTON_TEXT = 'Создать таблицу эксперимента'

@dataclass
class Layouts:
    main_inner_layout: QVBoxLayout
    main_layout: QGroupBox


@dataclass
class Buttons:
    create_table_button: QPushButton


class ControllersLayout:
    def __init__(self):
        self.main_layout = self.build_main_layout()

    def build_main_layout(self):
        layouts = get_elements(Layouts)
        buttons = get_elements(Buttons, [CREATE_TABLE_BUTTON_TEXT])

        return self.makeup(layouts, buttons)

    @staticmethod
    def makeup(layouts, buttons):
        layouts.main_inner_layout.addWidget(buttons.create_table_button)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout
