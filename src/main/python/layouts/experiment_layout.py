from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGroupBox, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QLayout
from dataclasses import dataclass, fields

from layouts import BaseLayout

TITLE = 'Числовые данные эксперимента'
X = 'x'
DELTA1 = 'Δ1'
DELTA2 = 'Δ2'


@dataclass
class Layouts:
    col0_layout: QVBoxLayout
    col1_layout: QVBoxLayout
    col2_layout: QVBoxLayout
    col3_layout: QVBoxLayout

    title_layout: QHBoxLayout
    table_layout: QHBoxLayout
    main_inner_layout: QVBoxLayout
    main_layout: QGroupBox


@dataclass
class Labels:
    title_label: QLabel


@dataclass
class ZeroCol:
    row0_label: QLabel
    row1_label: QLabel
    row2_label: QLabel
    row3_label: QLabel
    row4_label: QLabel
    row5_label: QLabel
    row6_label: QLabel
    row7_label: QLabel
    row8_label: QLabel
    row9_label: QLabel


@dataclass
class FirstCol:
    x_label: QLabel
    line11: QLineEdit
    line12: QLineEdit
    line13: QLineEdit
    line14: QLineEdit
    line15: QLineEdit
    line16: QLineEdit
    line17: QLineEdit
    line18: QLineEdit
    line19: QLineEdit


@dataclass
class SecondCol:
    delta1_label: QLabel
    line21: QLineEdit
    line22: QLineEdit
    line23: QLineEdit
    line24: QLineEdit
    line25: QLineEdit
    line26: QLineEdit
    line27: QLineEdit
    line28: QLineEdit
    line29: QLineEdit


@dataclass
class ThirdCol:
    delta2_label: QLabel
    line31: QLineEdit
    line32: QLineEdit
    line33: QLineEdit
    line34: QLineEdit
    line35: QLineEdit
    line36: QLineEdit
    line37: QLineEdit
    line38: QLineEdit
    line39: QLineEdit


class ExperimentLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        labels = self.utils.get_elements(Labels, [TITLE])
        column0_elements = self.utils.get_elements(
            ZeroCol, [''] + list(map(str, range(1, 10))))
        column1_elements = self.utils.get_elements(FirstCol, [X])
        column2_elements = self.utils.get_elements(SecondCol, [DELTA1])
        column3_elements = self.utils.get_elements(ThirdCol, [DELTA2])

        self.set_validators(column0_elements)
        self.set_validators(column1_elements)
        self.set_validators(column2_elements)
        self.set_validators(column3_elements)

        self.set_labels_alignment(labels)

        return self.compose_layout(layouts,
                                   labels,
                                   column0_elements,
                                   column1_elements,
                                   column2_elements,
                                   column3_elements)

    def compose_layout(self,
                       layouts: Layouts,
                       labels: Labels,
                       column0_elements: ZeroCol,
                       column1_elements: FirstCol,
                       column2_elements: SecondCol,
                       column3_elements: ThirdCol):

        layouts.title_layout.addWidget(labels.title_label)

        self.add_widgets(layouts.col0_layout, column0_elements)
        self.add_widgets(layouts.col1_layout, column1_elements)
        self.add_widgets(layouts.col2_layout, column2_elements)
        self.add_widgets(layouts.col3_layout, column3_elements)

        layouts.table_layout.addLayout(layouts.col0_layout)
        layouts.table_layout.addLayout(layouts.col1_layout)
        layouts.table_layout.addLayout(layouts.col2_layout)
        layouts.table_layout.addLayout(layouts.col3_layout)

        layouts.main_inner_layout.addLayout(layouts.title_layout)
        layouts.main_inner_layout.addLayout(layouts.table_layout)
        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    @staticmethod
    def add_widgets(layout: QLayout, widgets: dataclass):
        """Method to add widgets on the layout

        :param layout: layout to add widgets on
        :param widgets: dataclass of widgets
        """
        return [layout.addWidget(getattr(widgets, element.name))
                for element in fields(widgets)]

    def set_labels_alignment(self,
                             labels: Labels,
                             alignment: Qt.Alignment = Qt.AlignCenter):
        """Method to set labels alignment

        :param labels: labels to set the alignment
        :param alignment: default labels alignment
        """
        self.utils.set_alignment(labels.title_label, alignment)

    def set_validators(self, lines: dataclass, regex: str = r"[-+]?\d*\.\d+|\d+"):
        """Method to set validators to the QLineEdit objects

        :param lines: dataclass with the QLineEdit objects
        :param regex: regex string to set for validator
        """
        only_numbers_validator = self.utils.get_validator(regex)

        for field in fields(lines):
            # to avoid widgets with no setValidator method because the Lines dataclasses
            # have also the QLabel widgets
            try:
                getattr(lines, field.name).setValidator(only_numbers_validator)
            except AttributeError:
                pass
