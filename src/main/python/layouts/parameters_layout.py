from PySide2.QtWidgets import QGroupBox, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit
from dataclasses import dataclass

from layouts import BaseLayout

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
    factors: QLineEdit
    experiments: QLineEdit

    def get_lines(self):
        return [self.factors, self.experiments]


class ParametersLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_main_layout()

    def build_main_layout(self):
        layouts = self.utils.get_elements(Layouts)
        lines = self.utils.get_elements(Lines)
        labels = self.utils.get_elements(Labels, [FACTORS_LABEL_TEXT, FACTORS_LABEL_RANGE,
                                       EXPERIMENTS_LABEL_TEXT, EXPERIMENTS_LABEL_RANGE])

        self.set_labels_color(labels)
        self.set_lines_size(lines)
        self.set_lines_validators(lines)

        self.connect_handler(lines)
        return self.makeup(layouts, labels, lines)

    @staticmethod
    def makeup(layouts, labels, lines):
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

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    def connect_handler(self, lines):
        lines.factors.textEdited.connect(
            lambda: self.controllers.disable_experiments_cells_by_number_of_factors(
                self.main_layout,
                self.experiment,
                lines.factors.text()))
        lines.experiments.textEdited.connect(
            lambda: self.controllers.set_number_of_experiments(
                self.experiment,
                lines.experiments.text()))

    def set_lines_validators(self, lines):
        factors_validator = self.utils.get_validator(FACTORS_REGEX)
        experiments_validator = self.utils.get_validator(EXPERIMENTS_REGEX)

        lines.factors.setValidator(factors_validator)
        lines.experiments.setValidator(experiments_validator)

    def set_labels_color(self, labels):
        self.utils.set_style_sheet(labels.experiments_range_label, RANGE_LABELS_COLOR)
        self.utils.set_style_sheet(labels.factors_range_label, RANGE_LABELS_COLOR)

    def set_lines_size(self, lines):
        for line in lines.get_lines():
            self.utils.set_size(line, LINES_SIZE)
