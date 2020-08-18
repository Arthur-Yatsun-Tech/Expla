from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from dataclasses import dataclass

from layouts import BaseLayout

STUDENT_NAME = 'Критерий Стьюдента'
FISHER_NAME = 'Критерий Фишера'


@dataclass
class Layouts:
    student_layout: QHBoxLayout
    fisher_layout: QHBoxLayout
    main_inner_layout: QVBoxLayout
    main_layout: QGroupBox


@dataclass
class Labels:
    student_name_label: QLabel
    fisher_name_label: QLabel
    student_result_label: QLabel
    fisher_result_label: QLabel


class CriteriaLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        labels = self.utils.get_elements(Labels, [STUDENT_NAME, FISHER_NAME])

        return self.compose_layout(layouts, labels)

    @staticmethod
    def compose_layout(layouts, labels):
        layouts.student_layout.addWidget(labels.student_name_label)
        layouts.student_layout.addWidget(labels.student_result_label)

        layouts.fisher_layout.addWidget(labels.fisher_name_label)
        layouts.fisher_layout.addWidget(labels.fisher_result_label)

        layouts.main_inner_layout.addLayout(layouts.student_layout)
        layouts.main_inner_layout.addLayout(layouts.fisher_layout)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout
