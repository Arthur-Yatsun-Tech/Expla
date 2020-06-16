from math import sqrt

import pandas as pd


class Statistics:
    def __init__(self, experiments_data):
        self.experiments = experiments_data

    def calculate(self):
        mean = []
        variation = []
        std = []
        t = []

        for experiment in zip(*self.experiments):
            mean.append(self.calculate_mean(experiment))
            variation.append(self.calculate_dispersion(experiment, mean[-1]))
            std.append(sqrt(variation[-1]))

        max_std = max(std)
        for experiment in zip(*self.experiments):
            t.append((max(experiment) - self.calculate_mean(experiment)) /
                     sqrt(max_std))

        return pd.DataFrame({'mean': mean, 'variation': variation, 'std': std, 't': t}).round(3)

    @staticmethod
    def calculate_mean(data):
        return sum(data) / len(data)

    @staticmethod
    def calculate_dispersion(data, mean):
        sum_ = 0
        for element in data:
            sum_ += (element - mean) ** 2
        return sum_ / (len(data) - 1)
