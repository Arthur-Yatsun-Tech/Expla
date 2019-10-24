from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget

from controllers.table_window.elements.buttons import calculate_data
from controllers.table_window.elements.table import set_plan, fill_random_numbers, get_experiments_data
from table_planning.table_planer import TablePlanner


def init_layouts(self):
    widget = QWidget()
    self.showMaximized()
    self.plan = TablePlanner(self.levels, self.factors).create_table()

    main_layout = QVBoxLayout()
    button_layout = init_button_layout(self)
    self.table = init_table_layout(self.rows, self.columns, self.factors, self.experiments, self.plan)

    set_plan(self.table, self.plan, self.factors, self.rows)

    main_layout.addWidget(self.table)
    main_layout.addLayout(button_layout)

    widget.setLayout(main_layout)
    return widget


def init_table_layout(rows, columns, factors, experiments, plan):
    table = QTableWidget()
    table.setRowCount(rows)
    table.setColumnCount(columns)

    table.setHorizontalHeaderLabels(_get_header_labels(factors, experiments, plan))
    [table.setColumnWidth(i, 50) for i in range(columns)]
    return table


def init_button_layout(self):
    button_layout = QHBoxLayout()

    save_button = QPushButton('Сохранить')
    calculate_button = QPushButton('Посчитать')
    continue_button = QPushButton('Продолжить')

    calculate_button.clicked.connect(lambda: calculate_data(self))

    button_layout.addWidget(save_button)
    button_layout.addWidget(calculate_button)
    button_layout.addWidget(continue_button)

    return button_layout


def disable_parent(parent, mode=False):
    parent.number_of_experiments.setEnabled(mode)
    parent.number_of_factors.setEnabled(mode)
    parent.level_5.setEnabled(mode)
    parent.level_3.setEnabled(mode)
    parent.level_2.setEnabled(mode)
    [column.setEnabled(mode) for column in parent.rows_edit_x]
    [column.setEnabled(mode) for column in parent.rows_edit_d1]
    [column.setEnabled(mode) for column in parent.rows_edit_d2]
    parent.export_table_button.setEnabled(mode)
    parent.import_table_button.setEnabled(mode)
    parent.open_table_button.setEnabled(mode)


def _get_header_labels(factors, experiments, plan):
    x_s = [f'x{i + 1}' for i in range(factors)]
    y_s = [f'y{i + 1}' for i in range(experiments)]
    var_s = ['', 'mean', 'disp', 'std']
    headers = x_s + y_s + var_s
    return headers
