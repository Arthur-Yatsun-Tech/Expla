from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGroupBox, QRadioButton, QLabel, QVBoxLayout, QHBoxLayout
from dataclasses import dataclass

from controllers.main_window.elements.radios import set_level
from layouts.utils import get_qradio, get_qlabel, set_alignment, get_elements


@dataclass
class Layouts:
    radio_layout: QVBoxLayout
    main_inner_layout: QHBoxLayout
    main_layout: QGroupBox


@dataclass
class Labels:
    levels_label: QLabel


@dataclass
class Radios:
    level2: QRadioButton
    level3: QRadioButton
    level5: QRadioButton


class LevelsLayout:
    def __init__(self):
        self.main_layout = self.build_main_layout()

    def build_main_layout(self):
        labels = self.get_labels()
        radios = self.get_radios()
        layouts = get_elements(Layouts)

        self.set_elements_alignment(labels, layouts)
        # TODO: connection
        # self.connect_handler(radios)

        return self.makeup(layouts, radios, labels)

    @staticmethod
    def makeup(layouts, radios, labels):
        layouts.radio_layout.addWidget(radios.level2)
        layouts.radio_layout.addWidget(radios.level3)
        layouts.radio_layout.addWidget(radios.level5)

        layouts.main_inner_layout.addWidget(labels.levels_label)
        layouts.main_inner_layout.addLayout(layouts.radio_layout)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        return layouts.main_layout

    @staticmethod
    def set_elements_alignment(labels, layouts):
        set_alignment(labels.levels_label, Qt.AlignCenter)
        set_alignment(layouts.radio_layout, Qt.AlignRight)

    def connect_handler(self, radios):
        radios.level5.clicked.connect(
            lambda: set_level(self, radios.level5.text()))
        radios.level3.clicked.connect(
            lambda: set_level(self, radios.level3.text()))
        radios.level2.clicked.connect(
            lambda: set_level(self, radios.level2.text()))

    @staticmethod
    def get_radios():
        return Radios(
            level2=get_qradio('2'),
            level3=get_qradio('3'),
            level5=get_qradio('5'))

    @staticmethod
    def get_labels():
        return Labels(
            get_qlabel('Количество уровней\n варьирования'))

