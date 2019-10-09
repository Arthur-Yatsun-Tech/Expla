import numpy as np


def calculate_data(table, y):
    y = list(zip(*y))
    y = np.array(y).astype(np.float)

    mean = [np.mean(row) for row in y]
    var = [np.var(row) for row in y]
    std = [np.std(row) for row in y]
