import numpy as np

from layouts.controllers.table_window.elements.table import fill_calculated_data, get_experiments_data


def calculate_data(self):
    y = get_experiments_data(self.experiments, self.rows, self.factors, self.table)

    y = list(zip(*y))
    y = np.array(y).astype(np.float)

    self.mean = [np.mean(row) for row in y]
    self.var = [np.var(row) for row in y]
    self.std = [np.std(row) for row in y]

    fill_calculated_data(self)
