import itertools
from collections import deque, defaultdict
from copy import deepcopy
from math import sqrt
from typing import Tuple, List, Dict, Optional

from scipy.stats import t


class Calculator:
    """Class to do experiment calculations"""

    SUBTRACTION_SYMBOL = '-'
    ADD_SYMBOL = '+'
    ZERO_SYMBOL = '0'

    def __init__(self, experiment):
        """
        :param experiment: instance of the experiment
        """
        self.experiment = experiment

    def calculate_statistics(self, experiments_data: deque) -> Tuple[deque, deque, deque]:
        """Method to calculate statistics of the experiment - mean, variation, std

        :param experiments_data: numeric result of the experiments
        """
        mean = deque()
        variation = deque()
        std = deque()

        for experiment_row in zip(*experiments_data):
            mean.append(self._calculate_mean(experiment_row))
            variation.append(self._calculate_variation(experiment_row, mean[-1]))
            std.append(sqrt(variation[-1]))

        return mean, variation, std

    def calculate_student_criteria(self, experiments_data: deque) -> deque:
        """Method to calculate student criteria

        :param experiments_data: numeric result of the experiments
        """
        student_criteria = deque()

        for experiment_row in zip(*experiments_data):
            student_criteria.append(
                (max(experiment_row) - self._calculate_mean(experiment_row))
                / sqrt(self.experiment.max_variation_value))
        return student_criteria

    @staticmethod
    def _calculate_mean(data: Tuple) -> float:
        """Method to calculate mean value"""
        return sum(data) / len(data)

    @staticmethod
    def _calculate_variation(data: Tuple, mean: float) -> float:
        """Method to calculate variation value"""
        sum_ = 0
        for element in data:
            sum_ += (element - mean) ** 2
        return sum_ / (len(data) - 1)

    def calculate_regression_coeffs(self,
                                    experiments_plan: defaultdict,
                                    factors: int, mean: List[float],
                                    rows: int, round_value=4) -> Dict[str, List[float]]:
        """Method to calculate regression coefficients

        :param experiments_plan: plan of the experiment
        :param factors: experiment factors
        :param mean: the list of the mean values by each of the experiment rows
        :param rows: the count of the rows in the table (N value)
        :param round_value: value for round the regression coeffs
        """
        coeffs = {}
        regression_intervals = self.calculate_regression_intervals()

        plan = experiments_plan
        # create the list of tuples of the sorted columns of plan
        plan = [(key[-1], plan[key]) for key in sorted(plan.keys())]

        # get the b0 coeff
        coeffs['0'] = [
            round(sum(mean) / rows, round_value),
            regression_intervals.popleft(),
        ]
        for index in range(1, factors + 1):
            # create the combinations for columns in plan regarding the index value
            combinations = list(itertools.combinations(plan, index))

            for combination in combinations:
                converted_combination = self.convert_symbols_to_numbers(combination)
                coeff_name = ''
                # create coefficient name
                for data_column in converted_combination:
                    coeff_name += data_column[0]

                # get only the lists from the converted_combinations
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
                    zip(passing_combinations, mean)) / rows

                coeffs[coeff_name] = [
                    round(coeff_result, round_value),
                    regression_intervals.popleft(),
                ]
        return coeffs

    @staticmethod
    def optimize_regression_coeffs(regression_coeffs: Dict) -> Dict[str, List]:
        """Method to optimize regression coefficients

        :param regression_coeffs: counted regression coefficients
        """

        regression_coeffs = deepcopy(regression_coeffs)
        unoptimized_coeffs_keys = deque()

        for key, coeff_data in regression_coeffs.items():
            coeff, interval = coeff_data
            if abs(coeff) < abs(interval):
                unoptimized_coeffs_keys.append(key)

        # remove unoptimized coefficients and save it in new variable
        unoptimized_coeffs = \
            {key: regression_coeffs.pop(key, None) for key in unoptimized_coeffs_keys}

        return regression_coeffs, unoptimized_coeffs

    @staticmethod
    def distribute_the_reminder_from_unsuitable_coeffs(
            optimized_coeffs: Dict[str, List],
            unsuitable_coeffs: Dict[str, List]):
        """Method to distribute the reminder"""
        sum_of_unsuitable = sum(value[0] for value in unsuitable_coeffs.values())
        reminder = sum_of_unsuitable / len(unsuitable_coeffs)

        # distribute reminder
        for key in optimized_coeffs.keys():
            optimized_coeffs[key][0] += reminder

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

    def calculate_regression_intervals(self) -> deque:
        """Method to calculate regression intervals"""
        regression_intervals = deque()
        df = self.experiment.count_of_experiments - 1
        student_table_value = self.get_student_table_value(df, 0.025)

        for std in self.experiment.std:
            regression_intervals.append((student_table_value * std) /
                                        sqrt(self.experiment.rows))
        return regression_intervals

    @staticmethod
    def get_student_table_value(df, probability=0.025):
        """Method to get the table value of the student criteria

        :param df: degree of freedom
        :param probability: probability of the distribution from the one side:
            0.025 -> 0.005 in common
        """
        return abs(t.ppf(probability, df))
