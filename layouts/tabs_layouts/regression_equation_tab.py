from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from dataclasses import dataclass

from layouts import BaseLayout


@dataclass
class Layouts:
    main_inner_layout: QVBoxLayout
    main_layout: QWidget


@dataclass
class Labels:
    equation_label: QLabel


class RegressionEquationLayout(BaseLayout):
    """Class to create a regression equation tab"""

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        labels = self.utils.get_elements(Labels, ["Regression equation"])
        return self.compose_layout(layouts, labels)

    @staticmethod
    def compose_layout(layouts, labels):
        layouts.main_inner_layout.addWidget(labels.equation_label)
        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout
