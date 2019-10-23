from PySide2.QtWidgets import QLabel


def set_factors(self, factors):
    if factors in '':
        self.factors = 0
    else:
        self.factors = int(factors)

    if self.factors == 0:
        deleted_columns_count = 10 - self.main_layout.count()
        print(deleted_columns_count)

        for i in reversed(range(deleted_columns_count)):

            self.columns[::-1][i].addWidget(QLabel(f'{abs(i - 9)}'))
            self.columns[::-1][i].addWidget(self.rows_edit_x[::-1][i])
            self.columns[::-1][i].addWidget(self.rows_edit_d1[::-1][i])

            if self.levels == 5:
                self.columns[::-1][i].addWidget(self.rows_edit_d2[::-1][i])

            self.main_layout.addLayout(self.columns[::-1][i])
    else:
        current_factors = 9 - int(self.factors)
        [_deleteItemsOfLayout(self.columns[::-1][i]) for i in range(current_factors)]
        self.factors = 9 - current_factors


def set_experiments(self, text):
    self.experiments = int(text)


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
