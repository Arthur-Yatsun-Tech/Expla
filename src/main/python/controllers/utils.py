from PySide2.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem

from constants import VAR
from layouts.tabs_layouts.table_layout import COLUMNS


def set_enabled(element, mode=False):
    element.setEnabled(mode)


def cast_parameter_to_int(parameter):
    try:
        parameter = int(parameter)
    except ValueError:
        parameter = 0
    return parameter


def get_experiment_cells(current_layout):
    main_window = current_layout.parent()
    return main_window.children()[3].findChildren(QLineEdit)


def get_experiment_table(current_layout):
    main_window = current_layout.parent()
    tab_widget = main_window.children()[-1]
    return tab_widget.findChild(QTableWidget)


def set_experiment_plan(experiment, table, plan):
    if experiment.levels == 5 and experiment.factors >= 5:
        rows = experiment.factors * 25
    else:
        rows = experiment.levels ** experiment.factors

    for column, key in zip(range(experiment.factors), plan.keys()):
        for row in range(rows):
            table.setItem(row, column, QTableWidgetItem(
                plan[key][row]))


def set_table_headers(table, experiment):
    x = [f'x{i + 1}' for i in range(experiment.factors)]
    y = [f'y{i + 1}' for i in range(experiment.count_of_experiments)]
    labels = x + y + VAR
    [labels.append('') for _ in range(COLUMNS - len(labels))]

    table.setHorizontalHeaderLabels(labels)

