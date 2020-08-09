import itertools
from collections import deque
from math import sqrt
from typing import Tuple, List

from scipy.stats import t


class Calculator:

    SUBTRACTION_SYMBOL = '-'
    ADD_SYMBOL = '+'
    ZERO_SYMBOL = '0'

    def __init__(self, experiment):
        self.experiment = experiment
        self.mean = []
        self.variation = []
        self.std = []
        self.student_criteria = []

    def calculate_statistics(self):
        """Method to calculate statistics of the experiment - mean, variation, std"""
        for experiment_row in zip(*self.experiment.experiments_data):
            self.mean.append(self._calculate_mean(experiment_row))
            self.variation.append(self._calculate_dispersion(experiment_row, self.mean[-1]))
            self.std.append(sqrt(self.variation[-1]))

        self.experiment.set_mean(self.mean)
        self.experiment.set_variation(self.variation)
        self.experiment.set_std(self.std)

    def calculate_student_criteria(self):
        """Method to calculate student criteria"""
        for experiment_row in zip(*self.experiment.experiments_data):
            self.student_criteria.append(
                (max(experiment_row) - self._calculate_mean(experiment_row))
                / sqrt(self.experiment.max_variation_value))

        self.experiment.set_student_criteria(self.student_criteria)

    @staticmethod
    def _calculate_mean(data):
        return sum(data) / len(data)

    @staticmethod
    def _calculate_dispersion(data, mean):
        sum_ = 0
        for element in data:
            sum_ += (element - mean) ** 2
        return sum_ / (len(data) - 1)

    def calculate_regression_coeffs(self, round_value=4):
        """Method to calculate regression coefficients

        :param round_value: value for round the regression coeffs
        """
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

                coeffs[coeff_name] = round(coeff_result, round_value)

        # get the b0 coeff
        coeffs['0'] = round(sum(self.experiment.mean) / self.experiment.rows, round_value)
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

    def calculate_regression_intervals(self):
        pass

    @staticmethod
    def get_student_table_value(df, probability):
        """Method to get the table value of the student criteria

        :param df: degree of freedom
        :param probability: probability of the distribution from the one side:
            0.025 -> 0.005 in common
        """
        return abs(t.ppf(probability, df))
