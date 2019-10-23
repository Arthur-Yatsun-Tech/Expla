import re


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())
        layout.setParent(None)


def set_factors(self, factors):
    self.factors = factors
    print(self.factors)
    # if re.findall(r'[^2-9]|[2-9]\w', self.factors):
    #     self.number_of_factors.setText('')
    #     self.factors = ''
    #
    # columns = self.columns[::-1]
    # rows_edit_x = self.rows_edit_x[::-1]
    # rows_edit_d1 = self.rows_edit_d1[::-1]
    # rows_edit_d2 = self.rows_edit_d2[::-1]
    #
    # if self.factors in '':
    #     self.factors = 0
    #     deleted_columns_count = 10 - self.bottom_left_layout.count()
    #     for i in reversed(range(deleted_columns_count)):
    #         if self.levels == 2 or self.levels == 3:
    #
    #             self._add_widgets_into_column(
    #                 columns[i],
    #                 f'{abs(i - 9)}',
    #                 rows_edit_x[i],
    #                 rows_edit_d1[i],
    #             )
    #         else:
    #             self._add_widgets_into_column(
    #                 columns[i],
    #                 f'{abs(i - 9)}',
    #                 rows_edit_x[i],
    #                 rows_edit_d1[i],
    #                 rows_edit_d2[i]
    #             )
    #         self.bottom_left_layout.addLayout(columns[i])
    # else:
    #     current_factors = 9 - int(self.factors)
    #     [deleteItemsOfLayout(columns[i]) for i in range(current_factors)]
    #     self.factors = 9 - current_factors


def set_experiments(self, text):
    print(text)
    # is_string = re.findall(r'\D', text)
    #
    # if not is_string:
    #     self.experiments = int(int(text))
    # else:
    #     self.number_of_experiments.setText('')
    #     self.experiments = 0
