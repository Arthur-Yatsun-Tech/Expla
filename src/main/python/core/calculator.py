import itertools
from collections import deque
from math import sqrt
from typing import Tuple, List

import pandas as pd
from scipy.stats import t


class Calculator:

    SUBTRACTION_SYMBOL = '-'
    ADD_SYMBOL = '+'
    ZERO_SYMBOL = '0'

    def __init__(self, experiment):
        self.experiment = experiment

    def calculate_statistics(self) -> pd.DataFrame:
        mean = []
        variation = []
        std = []
        student_criteria = []

        for experiment in zip(*self.experiment.experiments_data):
            mean.append(self.calculate_mean(experiment))
            variation.append(self.calculate_dispersion(experiment, mean[-1]))
            std.append(sqrt(variation[-1]))

        max_variation = max(variation)
        for experiment in zip(*self.experiment.experiments_data):
            print(experiment)
            student_criteria.append((max(experiment) - self.calculate_mean(experiment)) /
                     sqrt(max_variation))

        self.experiment.set_mean(mean)
        self.experiment.set_variation(variation)
        self.experiment.set_std(std)
        self.experiment.set_student_criteria(student_criteria)

        return pd.DataFrame(
            {'mean': mean,
             'variation': variation,
             'std': std,
             't': student_criteria})

    @staticmethod
    def calculate_mean(data):
        return sum(data) / len(data)

    @staticmethod
    def calculate_dispersion(data, mean):
        sum_ = 0
        for element in data:
            sum_ += (element - mean) ** 2
        return sum_ / (len(data) - 1)

    def calculate_regression_coeffs(self):
        coeffs = {}

        plan = self.experiment.experiments_plan
        plan = [(key[-1], plan[key]) for key in sorted(plan.keys())]

        for index in range(1, self.experiment.factors + 1):
            # create the combinations for columns in plan regarding the index value
            combinations = list(itertools.combinations(plan, index))

            for combination in combinations:
                converted_combination = self.convert_symbols_to_numbers(combination)
                coeff_name = ''

                # create coefficient name
                for data_column in converted_combination:
                    coeff_name += data_column[0]

                # get only the lists from the converted_combinatins
                combination_arrays = list(map(lambda x: x[1], converted_combination))
                passing_combinations = []

                # create passing table values
                for row_elements in zip(*combination_arrays):
                    result = 1
                    for element in row_elements:
                        result *= element
                    passing_combinations.append(result)

                # count coefficients
                coeff_result = sum(comb * ex_mean for comb, ex_mean in
                    zip(passing_combinations, self.experiment.mean)) / self.experiment.rows

                coeffs[coeff_name] = round(coeff_result, 4)

        # get the b0 coeff
        coeffs['0'] = sum(self.experiment.mean) / self.experiment.rows
        self.experiment.set_regression_coeffs(coeffs)

    def convert_symbols_to_numbers(self, combinations: Tuple[Tuple[str, List]]) -> deque:
        """Method to convert symbols from the experiment plan into the numbers to
            count the regression coefficients
        :param combinations: combinations of the columns of the experiment plan in format
            (('1', ['-', '+'.. ]), ('2', ['-', '-'])) where '1' and '2' are numbers of the
            columns
        :return the deque in the format deque([('1', [-1, 1..], ), (('2', [-1, -1..])..)])
        """
        combinations_result = deque()
        for combination in combinations:
            result = deque()
            for symbol in combination[1]:
                if symbol == self.SUBTRACTION_SYMBOL:
                    result.append(-1)
                elif symbol == self.ADD_SYMBOL:
                    result.append(1)
                elif symbol == self.ZERO_SYMBOL:
                    result.append(0)
            combinations_result.append((combination[0], result))
        return combinations_result


class Criteria:
    """"""

    @staticmethod
    def get_student_table_value(df):
        return abs(t.ppf(0.025, df))
