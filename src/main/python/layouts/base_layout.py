from PySide2.QtWidgets import QGridLayout, QWidget
from dataclasses import dataclass

from layouts.controllers_layout import ControllersLayout
from layouts.experiment_layout import ExperimentLayout
from layouts.levels_layout import LevelsLayout
from layouts.parameters_layout import ParametersLayout
from layouts.tabs_layouts.base_tab_layout import BaseTabLayout
from layouts.utils import get_elements


@dataclass
class Layouts:
    main_inner_layout: QGridLayout
    main_layout: QWidget


class BaseLayout:
    def __init__(self):
        self.main_layout = self.build_result()

    def build_result(self):
        layouts = get_elements(Layouts)
        layouts.main_inner_layout.setColumnStretch(0, 1)
        layouts.main_inner_layout.setColumnStretch(1, 3)

        return self.makeup(layouts)

    @staticmethod
    def makeup(layouts):
        parameters_layout = ParametersLayout().main_layout
        levels_layout = LevelsLayout().main_layout
        experiment_layout = ExperimentLayout().main_layout
        controllers_layout = ControllersLayout().main_layout
        base_tab_layout = BaseTabLayout().main_layout

        # addWidget params:
        # widget, row, columns, stretching rows, stretching columns
        layouts.main_inner_layout.addWidget(parameters_layout, 1, 0)
        layouts.main_inner_layout.addWidget(levels_layout, 2, 0)
        layouts.main_inner_layout.addWidget(experiment_layout, 3, 0)
        layouts.main_inner_layout.addWidget(controllers_layout, 4, 0)
        layouts.main_inner_layout.addWidget(base_tab_layout, 1, 1, 4, 1)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout
