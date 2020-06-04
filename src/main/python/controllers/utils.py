import collections
import random

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QGroupBox, QLabel

from constants import VAR, COLORS, CURRENT_PARAMETER_COLOR
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
    for column, key in zip(range(experiment.factors), plan.keys()):
        for row in range(experiment.rows):
            table.setItem(row, column, QTableWidgetItem(
                plan[key][row]))

    set_table_headers(experiment, table)
    # TODO: algorithm to set color
    # set_table_color(experiment, table)
    # TODO: remove this
    fill_random_numbers(experiment, table)


def set_table_headers(experiment, table):
    x = [f'x{i + 1}' for i in range(experiment.factors)]
    y = [f'y{i + 1}' for i in range(experiment.count_of_experiments)]
    labels = x + y + VAR
    [labels.append('') for _ in range(COLUMNS - len(labels))]

    table.setHorizontalHeaderLabels(labels)


def set_table_color(experiment, table):
    if not (experiment.levels == 5 and experiment.factors >= 5):
        for columns in range(experiment.factors, 0, -1):
            for column in range(columns):
                if columns == 1:
                    break
                for row in range(experiment.levels ** columns):
                    table.item(1, 1).setBackgroundColor(QColor(*COLORS[columns]))
    else:
        for columns in range(experiment.factors, 0, -1):
            for column in range(experiment.factors):
                for row in range(25 * columns - 25, 25 * columns):
                    table.item(row, column).setBackgroundColor(QColor(*COLORS[columns]))

            for row in range(25 * columns - 25, 25 * columns):
                table.item(row, columns - 1).setBackgroundColor(QColor(*CURRENT_PARAMETER_COLOR))


def fill_random_numbers(experiment, table):
    for column in range(experiment.count_of_experiments):
        for row in range(experiment.rows):
            table.setItem(row, column + experiment.factors, QTableWidgetItem(str(random.randint(-100, 100))))


def get_experiments_data(experiment, table):
    for column in range(experiment.count_of_experiments):
        column_data = collections.deque()
        for row in range(experiment.rows):
            column_data.append(
                float(table.item(row, column + experiment.factors).text()))
        experiment.experiments_data.append(column_data)


def set_statistics(table, experiment, statistics):
    start_column = experiment.factors + experiment.count_of_experiments + 1
    for row in range(experiment.rows):
        table.setItem(row, start_column, QTableWidgetItem(
            str(statistics['mean'][row])))
        table.setItem(row, start_column+1, QTableWidgetItem(
            str(statistics['variation'][row])))
        table.setItem(row, start_column+2, QTableWidgetItem(
            str(statistics['std'][row])))
        table.setItem(row, start_column+3, QTableWidgetItem(
            str(statistics['t'][row])))


def set_criteria(current_layout, experiment, t_max):
    t_table = experiment.get_student_cirteria()

    main_window = current_layout.parent()
    tab_widget = main_window.children()[-1]
    critera_widget = tab_widget.findChildren(QGroupBox)[0]
    labels = critera_widget.findChildren(QLabel)

    student_result_label = labels[1]
    fisher_result_label = labels[2]

    result = 'соблюдается' if t_max < t_table else \
             'не соблюдается'

    student_result_label.setText(
        f't-табличное (α=0.05, df={experiment.count_of_experiments-1}):\n'
        f'{t_table}\n'
        f'Максимальное расчетное значение:\n'
        f'{t_max}\n\n'
        f'Условие t-расчетное < t-табличное {result}')