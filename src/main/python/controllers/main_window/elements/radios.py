from PySide2.QtWidgets import QLabel

from controllers.main_window.elements.qlines import set_disabled


def set_level(self, text):
    print(text)
    set_disabled(self, mode=True)
    self.levels = int(text)

    if self.levels == 2 or self.levels == 3:
        try:
            self.columns[0].itemAt(3).widget().setParent(None)
        except AttributeError:
            pass

        if self.factors == 0:
            [self.rows_edit_d2[i].setParent(None) for i in range(9)]
        else:
            [self.rows_edit_d2[i].setParent(None) for i in range(self.factors)]

    else:
        if self.columns[0].count() < 4:
            self.columns[0].addWidget(QLabel('delta 2'))

        if self.factors == 0:
            [self.columns[i + 1].addWidget(self.rows_edit_d2[i]) for i in range(9)]
        else:
            [self.columns[i + 1].addWidget(self.rows_edit_d2[i]) for i in range(self.factors)]
