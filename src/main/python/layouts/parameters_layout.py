import PySide2
from PySide2.QtWidgets import QGroupBox, QLabel, QHBoxLayout, QVBoxLayout
from dataclasses import dataclass

from controllers.main_window.elements.qlines import set_factors, set_experiments
from layouts.utils import get_qlabel, get_qline, set_size, get_validator, get_hbox, get_vbox, set_style_sheet, \
    get_elements

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
    experiments_labels_layout: QHBoxLayout
    factors_labels_layout: QHBoxLayout
    labels_layout: QVBoxLayout
    lines_layout: QVBoxLayout
    main_inner_layout: QHBoxLayout
    main_layout: QGroupBox


@dataclass
class Labels:
    factors_label: QLabel
    factors_range_label: QLabel
    experiments_label: QLabel
    experiments_range_label: QLabel


@dataclass
class Lines:
    factors: PySide2.QtWidgets.QLineEdit
    experiments: PySide2.QtWidgets.QLineEdit

    def get_lines(self):
        return [self.factors, self.experiments]


class ParametersLayout:
    def __init__(self):
        self.layouts = get_elements(Layouts)
        self.lines = get_elements(Lines)
        self.labels = self.get_labels()

        self.set_labels_color()
        self.set_lines_size()
        self.set_lines_validators()

        # TODO: remove self in handlers
        # self.connect_handler(lines)

    def makeup(self):
        self.layouts.experiments_labels_layout.addWidget(self.labels.experiments_label)
        self.layouts.experiments_labels_layout.addWidget(self.labels.experiments_range_label)

        self.layouts.factors_labels_layout.addWidget(self.labels.factors_label)
        self.layouts.factors_labels_layout.addWidget(self.labels.factors_range_label)

        self.layouts.labels_layout.addLayout(self.layouts.factors_labels_layout)
        self.layouts.labels_layout.addLayout(self.layouts.experiments_labels_layout)

        self.layouts.lines_layout.addWidget(self.lines.factors)
        self.layouts.lines_layout.addWidget(self.lines.experiments)

        self.layouts.main_inner_layout.addLayout(self.layouts.labels_layout)
        self.layouts.main_inner_layout.addLayout(self.layouts.lines_layout)

        self.layouts.main_layout.setLayout(self.layouts.main_inner_layout)
        return self.layouts.main_layout

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
