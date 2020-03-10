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
        self.labels = self.get_labels()
        self.radios = self.get_radios()
        self.layouts = get_elements(Layouts)

        self.set_elements_alignment()
        self.connect_handler()

    def makeup(self):
        pass

    def set_elements_alignment(self):
        set_alignment(self.labels.levels_label, Qt.AlignCenter)
        set_alignment(self.layouts.radio_layout, Qt.AlignRight)

    def connect_handler(self):
        self.radios.level5.clicked.connect(
            lambda: set_level(self, self.radios.level5.text()))
        self.radios.level3.clicked.connect(
            lambda: set_level(self, self.radios.level3.text()))
        self.radios.level2.clicked.connect(
            lambda: set_level(self, self.radios.level2.text()))

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

