def set_level(self, text):
    self.levels = int(text)
    if self.levels == 2 or self.levels == 3:
        if self.factors:
            self.column0_d2_label.setParent(None)
        [self.rows_edit_x[i].setParent(None) for i in range(self.factors)]
    else:
        self.columns[0].addWidget(self.column0_d2_label)

        if self.factors == 0:
            [self.columns[i+1].addWidget(self.rows_edit_x[i]) for i in range(9)]
        else:
            [self.columns[i+1].addWidget(self.rows_edit_x[i]) for i in range(self.factors)]
