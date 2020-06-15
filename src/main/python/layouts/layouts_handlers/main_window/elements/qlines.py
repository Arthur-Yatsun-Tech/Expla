import time

from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QLabel

X1 = slice(9)
D1 = slice(9, 18)
D2 = slice(18, 28)


def set_factors(main_layout, experiment, factors):
    main_window = main_layout.parent()
    experiment_cells = main_window.children()[3].findChildren(QLineEdit)
    experiment_labels = main_window.children()[3].findChildren(QLabel)

    layouts = main_window.children()[3].findChildren(QVBoxLayout)

    print(layouts[0].findChildren(QLineEdit))
    x1 = experiment_cells[X1]
    delta1 = experiment_cells[D1]
    delta2 = experiment_cells[D2]
    # children[0].setParent(None)

    # for i in x1:
    #     i.setParent(None)
    # if factors == '':
    #     for i in x1:
    #         i.setParent(main_layout)

    # qvbox = main_window.children()[3].findChildren(QVBoxLayout)
    # qvbox[2].addWidget(children[0])

    # for child in children:
    #     print(child.parent())
    # # print(main_window.count())

    experiment.factors = factors
    # self.level_5.setEnabled(True)
    # self.level_3.setEnabled(True)
    # self.level_2.setEnabled(True)
    #
    # if factors in '':
    #     self.factors = 0
    # else:
    #     self.factors = int(factors)
    #
    # if self.factors == 0:
    #     deleted_columns_count = 10 - self.table_layout.count()
    #
    #     for i in reversed(range(deleted_columns_count)):
    #         layout = QHBoxLayout()
    #         layout.addWidget(QLabel(f'{abs(i - 9)}'))
    #         layout.addWidget(self.rows_edit_x[::-1][i])
    #         layout.addWidget(self.rows_edit_d1[::-1][i])
    #
    #         if self.levels == 5:
    #             layout.addWidget(self.rows_edit_d2[::-1][i])
    #
    #         self.columns[::-1][i].addLayout(layout)
    #
    #         self.table_layout.addLayout(self.columns[::-1][i])
    # else:
    #     current_factors = 9 - int(self.factors)
    #     [_deleteItemsOfLayout(self.columns[::-1][i]) for i in range(current_factors)]
    #     self.factors = 9 - current_factors


def set_experiments(experiment, text):
    print(type(experiment.factors))
    # self.experiments = int(text)


def set_disabled(self, mode=False):
    for column, x, d1, d2 in zip(self.columns, self.rows_edit_x, self.rows_edit_d1, self.rows_edit_d2):
        column.setEnabled(mode)
        x.setEnabled(mode)
        d1.setEnabled(mode)
        d2.setEnabled(mode)


def _deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                _deleteItemsOfLayout(item.layout())
        layout.setParent(None)
