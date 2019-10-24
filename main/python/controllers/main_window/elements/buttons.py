from table import TableWindow


def save_table(self):
    print('save table')


def planning_table(self):
    table = TableWindow(self)
    table.show()


def set_buttons_disabled(self, mode=False):
    self.open_table_button.setEnabled(mode)
    self.import_table_button.setEnabled(mode)
    self.export_table_button.setEnabled(mode)