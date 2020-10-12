from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QGroupBox
from dataclasses import dataclass

from layouts import BaseLayout


@dataclass
class Layouts:
    equation_check_layout: QHBoxLayout
    regression_equation_layout: QHBoxLayout
    main_inner_layout: QVBoxLayout
    main_layout: QGroupBox


@dataclass
class Labels:
    equation_text_label: QLabel
    regression_equation_label: QLabel
    equation_check_label: QLabel


class RegressionEquationLayout(BaseLayout):
    """Class to create a regression equation tab"""

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        labels = self.utils.get_elements(Labels, ["Regression equation"])

        self.set_labels_alignment(labels)
        return self.compose_layout(layouts, labels)

    @staticmethod
    def compose_layout(layouts, labels):
        layouts.regression_equation_layout.addWidget(labels.equation_text_label)
        layouts.regression_equation_layout.addWidget(labels.regression_equation_label)

        labels.regression_equation_label.setText("asdf")
        layouts.equation_check_layout.addWidget(labels.equation_check_label)

        layouts.main_inner_layout.addLayout(layouts.regression_equation_layout)
        layouts.main_inner_layout.addLayout(layouts.equation_check_layout)
        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    def set_labels_alignment(self,
                             labels: Labels,
                             alignment: Qt.Alignment = Qt.AlignCenter):
        """Method to set labels alignment

        :param labels: labels to set the alignment
        :param alignment: default labels alignment
        """
        self.utils.set_alignment(labels.equation_text_label, alignment)
        self.utils.set_alignment(labels.regression_equation_label, alignment)
