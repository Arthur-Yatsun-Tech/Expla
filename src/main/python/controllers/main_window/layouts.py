from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QGroupBox, QLineEdit, QRadioButton, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGridLayout, QWidget, QTableWidget

from controllers.main_window.elements.buttons import planning_table, set_buttons_disabled
from controllers.main_window.elements.qlines import set_factors, set_experiments, set_disabled
from controllers.main_window.elements.radios import set_level


def init_layouts(self):
    widget = QWidget()

    enter_parameters_layout = _init_parameters_layout(self)
    choose_levels_layout = _init_levels_layout(self)
    parameters_table_layout = _init_parameters_table_layout(self)
    go_next_layout = _init_go_next_layout(self)

    table = QTableWidget()

    main_layout = QGridLayout()
    main_layout.addWidget(enter_parameters_layout, 1, 0)
    main_layout.addWidget(choose_levels_layout, 2, 0)
    main_layout.addWidget(parameters_table_layout, 3, 0)
    main_layout.addWidget(go_next_layout, 4, 0)
    main_layout.addWidget(table, 1, 1, 4, 1)

    main_layout.setColumnStretch(0, 1)
    main_layout.setColumnStretch(1, 3)

    widget.setLayout(main_layout)
    return widget


def _init_parameters_layout(self):
    experiment_parameters = QGroupBox()

    number_of_factors_label = QLabel("(1) Введите коло-во факторов")
    self.number_of_factors = QLineEdit()
    number_of_experiments_label = QLabel("(2) Введите коло-во серий экспериментов")
    self.number_of_experiments = QLineEdit()

    self.number_of_factors.textEdited.connect(lambda: set_factors(self, self.number_of_factors.text()))
    self.number_of_experiments.textEdited.connect(lambda: set_experiments(self, self.number_of_experiments.text()))

    factors_validator = QRegExpValidator(QRegExp(r"^[2-9]$"))
    self.number_of_factors.setValidator(factors_validator)
    experiments_validator = QRegExpValidator(QRegExp(r"^\d{3}$"))
    self.number_of_experiments.setValidator(experiments_validator)

    layout_1 = QVBoxLayout()
    layout_1.addWidget(number_of_factors_label)
    layout_1.addWidget(number_of_experiments_label)
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

    levels_label = QLabel('(3) Введите коло-во уровней')
    self.level_5 = QRadioButton('5')
    self.level_3 = QRadioButton('3')
    self.level_2 = QRadioButton('2')

    self.level_5.clicked.connect(lambda: set_level(self, self.level_5.text()))
    self.level_3.clicked.connect(lambda: set_level(self, self.level_3.text()))
    self.level_2.clicked.connect(lambda: set_level(self, self.level_2.text()))

    self.level_5.setEnabled(False)
    self.level_3.setEnabled(False)
    self.level_2.setEnabled(False)

    radio_group_layout = QHBoxLayout()
    radio_group_layout.addWidget(self.level_2)
    radio_group_layout.addWidget(self.level_3)
    radio_group_layout.addWidget(self.level_5)

    main_layout = QVBoxLayout()
    main_layout.addWidget(levels_label)
    main_layout.addLayout(radio_group_layout)

    experiment_levels_layout.setLayout(main_layout)
    return experiment_levels_layout


def _init_parameters_table_layout(self):
    parameters_table_layout = QGroupBox()
    main_layout = QVBoxLayout()
    self.table_layout = QHBoxLayout()

    title_layout = QVBoxLayout()
    title_layout.addWidget(QLabel("(4) Заполните данные об эксперименте\n"))

    self.columns = [QVBoxLayout() for _ in range(10)]
    self.rows_edit_x = [QLineEdit() for _ in range(9)]
    self.rows_edit_d1 = [QLineEdit() for _ in range(9)]
    self.rows_edit_d2 = [QLineEdit() for _ in range(9)]

    self.columns[0].addWidget(QLabel(''))
    self.columns[0].addWidget(QLabel('   x   '))
    self.columns[0].addWidget(QLabel('delta 1'))
    self.columns[0].addWidget(QLabel('delta 2'))

    for column in range(1, 10):
        self.columns[column].addWidget(QLabel(f'{column}'))
        self.columns[column].addWidget(self.rows_edit_x[column - 1])
        self.columns[column].addWidget(self.rows_edit_d1[column - 1])
        if self.rows_edit_d2[column - 1] is not None:
            self.columns[column].addWidget(self.rows_edit_d2[column - 1])

    self.rows_edit_x[0].textEdited.connect(lambda: set_buttons_disabled(self, mode=True))

    set_disabled(self, mode=False)
    [self.table_layout.addLayout(self.columns[column]) for column in range(10)]

    main_layout.addLayout(title_layout)
    main_layout.addLayout(self.table_layout)
    parameters_table_layout.setLayout(main_layout)
    return parameters_table_layout


def _init_go_next_layout(self):
    go_next_layout = QGroupBox()

    self.export_table_button = QPushButton('Сохранить таблицу')
    self.import_table_button = QPushButton('Загрузить таблицу')
    self.open_table_button = QPushButton('(5) Открыть таблицу эксперимента')

    self.open_table_button.clicked.connect(lambda: planning_table(self))
    self.import_table_button.setEnabled(False)

    layout1 = QHBoxLayout()
    layout1.addWidget(self.import_table_button)
    layout1.addWidget(self.export_table_button)

    main_layout = QVBoxLayout()
    main_layout.addWidget(self.open_table_button)
    main_layout.addLayout(layout1)

    set_buttons_disabled(self, mode=False)
    go_next_layout.setLayout(main_layout)
    return go_next_layout