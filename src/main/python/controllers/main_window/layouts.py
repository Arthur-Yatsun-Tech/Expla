from PySide2 import QtCore
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QGroupBox, QLineEdit, QRadioButton, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGridLayout, QWidget, QTableWidget, QTabWidget

from controllers.main_window.elements.buttons import planning_table, set_buttons_disabled
from controllers.main_window.elements.qlines import set_factors, set_experiments, set_disabled
from controllers.main_window.elements.radios import set_level
from layouts.experiment_layout import ExperimentLayout
from layouts.levels_layout import LevelsLayout
from layouts.parameters_layout import ParametersLayout


def init_layouts(self):
    widget = QWidget()

    enter_parameters_layout = ParametersLayout().main_layout
    choose_levels_layout = LevelsLayout().main_layout
    parameters_table_layout = ExperimentLayout().main_layout
    # parameters_table_layout = _init_parameters_table_layout(self)
    go_next_layout = _init_go_next_layout(self)

    table = QTableWidget()
    table.setRowCount(100)
    table.setColumnCount(100)
    [table.setColumnWidth(i, 50) for i in range(100)]

    tabs = QTabWidget()
    tab1 = QWidget()
    tab2 = QWidget()
    tab3 = QWidget()
    tab4 = QWidget()

    tabs.addTab(table, 'Таблица эксперемента')
    tabs.addTab(tab1, 'Критерии')
    tabs.addTab(tab2, 'Коэфициенты регрессии')
    tabs.addTab(tab3, 'Графики')
    tabs.addTab(tab4, 'Регрессионное уравнение')


    main_layout = QGridLayout()
    main_layout.addWidget(enter_parameters_layout, 1, 0)
    main_layout.addWidget(choose_levels_layout, 2, 0)
    main_layout.addWidget(parameters_table_layout, 3, 0)
    main_layout.addWidget(go_next_layout, 4, 0)
    main_layout.addWidget(tabs, 1, 1, 4, 1)

    main_layout.setColumnStretch(0, 1)
    main_layout.setColumnStretch(1, 3)

    widget.setLayout(main_layout)
    return widget


def _init_parameters_layout(self):
    experiment_parameters = QGroupBox()

    number_of_factors_label = QLabel("Количество факторов")
    number_of_factors_range = QLabel("[2 - 9]")
    number_of_factors_range.setStyleSheet('color: grey')

    self.number_of_factors = QLineEdit()
    self.number_of_factors.setFixedSize(30, 20)
    number_of_experiments_label = QLabel("Количество серий \nэкспериментов")
    number_of_experiments_range = QLabel("[2 - 999]")
    number_of_experiments_range.setStyleSheet('color: grey')

    self.number_of_experiments = QLineEdit()
    self.number_of_experiments.setFixedSize(30, 20)

    self.number_of_factors.textEdited.connect(lambda: set_factors(self, self.number_of_factors.text()))
    self.number_of_experiments.textEdited.connect(lambda: set_experiments(self, self.number_of_experiments.text()))

    factors_validator = QRegExpValidator(QRegExp(r"^[2-9]$"))
    self.number_of_factors.setValidator(factors_validator)
    experiments_validator = QRegExpValidator(QRegExp(r"^\d{3}$"))
    self.number_of_experiments.setValidator(experiments_validator)

    factor_layout = QHBoxLayout()
    factor_layout.addWidget(number_of_factors_label)
    factor_layout.addWidget(number_of_factors_range)

    experiment_layout = QHBoxLayout()
    experiment_layout.addWidget(number_of_experiments_label)
    experiment_layout.addWidget(number_of_experiments_range)

    layout_1 = QVBoxLayout()
    layout_1.addLayout(factor_layout)
    layout_1.addLayout(experiment_layout)
    layout_2 = QVBoxLayout()
    layout_2.addWidget(self.number_of_factors)
    layout_2.addWidget(self.number_of_experiments)

    main_layout = QHBoxLayout()
    main_layout.addLayout(layout_1)
    main_layout.addLayout(layout_2)

    experiment_parameters.setLayout(main_layout)
    return experiment_parameters


def _init_levels_layout(self):
    experiment_levels_layout = QGroupBox()

    levels_label = QLabel('Количество уровней\n варьирования')
    levels_label.setAlignment(QtCore.Qt.AlignCenter)

    self.level_5 = QRadioButton('5')
    self.level_3 = QRadioButton('3')
    self.level_2 = QRadioButton('2')

    self.level_5.clicked.connect(lambda: set_level(self, self.level_5.text()))
    self.level_3.clicked.connect(lambda: set_level(self, self.level_3.text()))
    self.level_2.clicked.connect(lambda: set_level(self, self.level_2.text()))

    # self.level_5.setEnabled(False)
    # self.level_3.setEnabled(False)
    # self.level_2.setEnabled(False)

    radio_group_layout = QVBoxLayout()
    radio_group_layout.setAlignment(QtCore.Qt.AlignRight)
    radio_group_layout.addWidget(self.level_2)
    radio_group_layout.addWidget(self.level_3)
    radio_group_layout.addWidget(self.level_5)

    main_layout = QHBoxLayout()
    main_layout.addWidget(levels_label)
    main_layout.addLayout(radio_group_layout)

    experiment_levels_layout.setLayout(main_layout)
    return experiment_levels_layout


def _init_parameters_table_layout(self):
    parameters_table_layout = QGroupBox()
    main_layout = QVBoxLayout()
    self.table_layout = QVBoxLayout()

    title_layout = QVBoxLayout()
    title_layout.addWidget(QLabel("Данные об эксперименте\n"))
    title_layout.setAlignment(QtCore.Qt.AlignCenter)

    self.columns = [QHBoxLayout() for _ in range(10)]
    self.rows_edit_x = [QLineEdit() for _ in range(9)]
    self.rows_edit_d1 = [QLineEdit() for _ in range(9)]
    self.rows_edit_d2 = [QLineEdit() for _ in range(9)]


    self.columns[0].addWidget(QLabel(''))
    layout = QHBoxLayout()
    layout.addWidget(QLabel('   x   '))
    layout.addWidget(QLabel('delta 1'))
    layout.addWidget(QLabel('delta 2'))

    self.columns[0].addLayout(layout)
    for column in range(1, 10):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f'{column}'))
        layout.addWidget(self.rows_edit_x[column - 1])
        layout.addWidget(self.rows_edit_d1[column - 1])
        if self.rows_edit_d2[column - 1] is not None:
            layout.addWidget(self.rows_edit_d2[column - 1])
        self.columns[column].addLayout(layout)

    self.rows_edit_x[0].textEdited.connect(lambda: set_buttons_disabled(self, mode=True))

    # set_disabled(self, mode=False)
    [self.table_layout.addLayout(self.columns[column]) for column in range(10)]

    main_layout.addLayout(title_layout)
    main_layout.addLayout(self.table_layout)
    parameters_table_layout.setLayout(main_layout)
    return parameters_table_layout


def _init_go_next_layout(self):
    go_next_layout = QGroupBox()

    # self.export_table_button = QPushButton('Сохранить таблицу')
    # self.import_table_button = QPushButton('Загрузить таблицу')
    self.open_table_button = QPushButton('Создать таблицу эксперимента')

    self.open_table_button.clicked.connect(lambda: planning_table(self))
    # self.import_table_button.setEnabled(False)

    # layout1 = QHBoxLayout()
    # layout1.addWidget(self.import_table_button)
    # layout1.addWidget(self.export_table_button)

    main_layout = QVBoxLayout()
    main_layout.addWidget(self.open_table_button)
    # main_layout.addLayout(layout1)

    set_buttons_disabled(self, mode=False)
    go_next_layout.setLayout(main_layout)
    return go_next_layout