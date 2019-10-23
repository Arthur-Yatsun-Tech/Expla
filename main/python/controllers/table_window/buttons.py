import numpy as np

from controllers.table_window.table import fill_calculated_data


def calculate_data(self):
    y = list(zip(*self.y))
    y = np.array(y).astype(np.float)

    self.mean = [np.mean(row) for row in y]
    self.var = [np.var(row) for row in y]
    self.std = [np.std(row) for row in y]

    fill_calculated_data(self)
