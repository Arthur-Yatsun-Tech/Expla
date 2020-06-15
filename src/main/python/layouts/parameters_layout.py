from PySide2.QtWidgets import QGroupBox, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit
from dataclasses import dataclass

from layouts.controllers.controllers import disable_experiments_cells_by_factor,\
    set_count_of_experiments
from layouts.base import BaseLayout
from layouts.utils import set_size, get_validator, set_style_sheet, get_elements

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
        layouts = get_elements(Layouts)
        lines = get_elements(Lines)
        labels = get_elements(Labels, [FACTORS_LABEL_TEXT, FACTORS_LABEL_RANGE,
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
            lambda: disable_experiments_cells_by_factor(
                self.main_layout,
                self.experiment,
                lines.factors.text()))
        lines.experiments.textEdited.connect(
            lambda: set_count_of_experiments(
                self.experiment,
                lines.experiments.text()))

    @staticmethod
    def set_lines_validators(lines):
        factors_validator = get_validator(FACTORS_REGEX)
        experiments_validator = get_validator(EXPERIMENTS_REGEX)

        lines.factors.setValidator(factors_validator)
        lines.experiments.setValidator(experiments_validator)

    @staticmethod
    def set_labels_color(labels):
        set_style_sheet(labels.experiments_range_label, RANGE_LABELS_COLOR)
        set_style_sheet(labels.factors_range_label, RANGE_LABELS_COLOR)

    @staticmethod
    def set_lines_size(lines):
        for line in lines.get_lines():
            set_size(line, LINES_SIZE)
