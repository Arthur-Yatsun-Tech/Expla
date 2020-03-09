import PySide2
from PySide2.QtWidgets import QGroupBox
from dataclasses import dataclass

from controllers.main_window.elements.qlines import set_factors, set_experiments
from layouts.utils import get_qlabel, get_qline, set_size, get_validator, get_hbox, get_vbox, set_style_sheet

FACTORS_REGEX = r"^[2-9]$"
EXPERIMENTS_REGEX = r"^\d{3}$"

FACTORS_LABEL_TEXT = "Количество факторов"
FACTORS_LABEL_RANGE = "[2 - 9]"
EXPERIMENTS_LABEL_TEXT = "Количество серий \nэкспериментов"
EXPERIMENTS_LABEL_RANGE = "[2 - 999]"

LINES_SIZE = (30, 20)
RANGE_LABELS_COLOR = 'color: grey'


@dataclass
class Layouts:
    experiments_labels_layout: PySide2.QtWidgets.QHBoxLayout
    factors_labels_layout: PySide2.QtWidgets.QHBoxLayout
    labels_layout: PySide2.QtWidgets.QVBoxLayout
    lines_layout: PySide2.QtWidgets.QVBoxLayout
    main_inner_layout: PySide2.QtWidgets.QHBoxLayout


@dataclass
class Labels:
    factors_label: PySide2.QtWidgets.QLabel
    factors_range_label: PySide2.QtWidgets.QLabel
    experiments_label: PySide2.QtWidgets.QLabel
    experiments_range_label: PySide2.QtWidgets.QLabel


@dataclass
class Lines:
    factors: PySide2.QtWidgets.QLineEdit
    experiments: PySide2.QtWidgets.QLineEdit

    def get_lines(self):
        return [self.factors, self.experiments]


class ParametersLayout:
    def __init__(self):
        self.main_layout = QGroupBox()
        self.layouts = self.get_layouts()
        self.labels = self.get_labels()
        self.lines = self.get_lines()

        self.set_labels_color()
        self.set_lines_size()
        self.set_lines_validators()

        # TODO: remove self in handlers
        # self.connect_handler(lines)

    def makeup(self, layouts, labels, lines):
        layouts.experiments_labels_layout.addWidget(labels.experiments_label)
        layouts.experiments_labels_layout.addWidget(labels.experiments_range_label)

        layouts.factors_labels_layout.addWidget(labels.factors_label)
        layouts.factors_labels_layout.addWidget(labels.factors_range_label)

        layouts.labels_layout.addLayout(layouts.factors_labels_layout)
        layouts.labels_layout.addLayout(layouts.experiments_labels_layout)

        layouts.lines_layout.addWidget(lines.factors)
        layouts.lines_layout.addWidget(lines.experiments)

        layouts.main_inner_layout.addLayout(layouts.labels_layout)
        layouts.main_inner_layout.addLayout(layouts.lines_layout)

        self.main_layout.setLayout(layouts.main_inner_layout)
        return self.main_layout

    def set_lines_validators(self):
        factors_validator = get_validator(FACTORS_REGEX)
        experiments_validator = get_validator(EXPERIMENTS_REGEX)

        self.lines.factors.setValidator(factors_validator)
        self.lines.experiments.setValidator(experiments_validator)

    def set_labels_color(self):
        set_style_sheet(self.labels.experiments_range_label, RANGE_LABELS_COLOR)
        set_style_sheet(self.labels.factors_range_label, RANGE_LABELS_COLOR)

    def connect_handler(self, lines):
        lines.factors.textEdited.connect(
            lambda: set_factors(
                self, lines.factors.text()))

        lines.experiments.textEdited.connect(
            lambda: set_experiments(
                self, lines.experiments.text()))

    def set_lines_size(self):
        for line in self.lines.get_lines():
            set_size(line, LINES_SIZE)

    @staticmethod
    def get_labels():
        return Labels(
            factors_label=get_qlabel(FACTORS_LABEL_TEXT),
            factors_range_label=get_qlabel(FACTORS_LABEL_RANGE),
            experiments_label=get_qlabel(EXPERIMENTS_LABEL_TEXT),
            experiments_range_label=get_qlabel(EXPERIMENTS_LABEL_RANGE))

    @staticmethod
    def get_lines():
        return Lines(
            factors=get_qline(),
            experiments=get_qline())

    @staticmethod
    def get_layouts():
        return Layouts(
            experiments_labels_layout=get_hbox(),
            factors_labels_layout=get_hbox(),
            labels_layout=get_vbox(),
            lines_layout=get_vbox(),
            main_inner_layout=get_hbox())
