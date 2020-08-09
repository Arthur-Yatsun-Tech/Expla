import collections
from typing import List, Optional, Dict

from core.calculator import Calculator


class Experiment:
    """The class to describe the experiment"""

    def __init__(self, factors: int = 9,
                 count_of_experiments: int = 3,
                 levels: int = 5,
                 experiments_data: Optional[List[collections.deque]] = None,
                 experiments_plan: Optional[collections.defaultdict] = None,
                 regression_coeffs: Optional[Dict] = None,
                 mean: Optional[List] = None,
                 variation: Optional[List] = None,
                 std: Optional[List] = None,
                 student_criteria: Optional[List] = None):
        """
        :param factors: number of the factors of the experiment `x` values
        :param count_of_experiments: number of the experiments_data `y` values
        :param levels: numbers of variations levels. possible values - [2, 3, 5]
        :param experiments_data: numeric data of the experiment according to the
                factors and count of the experiment
        :param experiments_plan: experiment table
        :param regression_coeffs: regression coefficients
        :param mean: mean value of the experiments
        :param variation: variation of the experiments
        :param std: standard derivation of the experiments
        :param student_criteria: student criteria of the experiments
        """
        self._calculator = Calculator(self)

        self.factors = factors
        self.count_of_experiments = count_of_experiments
        self.levels = levels

        # dynamic parameters
        self.experiments_data = experiments_data
        self.experiments_plan = experiments_plan
        self.regression_coeffs = regression_coeffs

        # statistics
        self.mean = mean
        self.variation = variation
        self.std = std
        self.student_criteria = student_criteria

        # TODO: Only for test proposals, remove it
        self.factors = 4
        self.count_of_experiments = 3
        self.levels = 2

    @property
    def rows(self):
        """Property to get the count of the rows in the table
            if the levels == 5 and the factors is greater or equals than 5 use the
            shortened table
        """
        return self.factors * 25 if self.levels == 5 and self.factors >= 5 else \
               self.levels ** self.factors

    @property
    def max_variation_value(self):
        """Property to get the max variation value from the variation list"""
        if self.variation:
            return max(self.variation)
        else:
            return 0

    @property
    def max_student_value(self):
        """Property to get the max value of the student criteria"""
        if self.student_criteria:
            return max(self.student_criteria)
        else:
            return 0

    def set_experiments_data(self, experiments_data: List[collections.deque]):
        """Method to set experiments data"""
        self.experiments_data = experiments_data

    def set_experiments_plan(self, experiments_plan: collections.defaultdict):
        """Method to set the experiments plan"""
        self.experiments_plan = experiments_plan

    def set_regression_coeffs(self, regression_coeffs: Dict):
        """Method to set regression coeffs"""
        self.regression_coeffs = regression_coeffs

    def set_mean(self, mean: List):
        """Method to set mean"""
        self.mean = mean

    def set_variation(self, variation: List):
        """Method to set variation"""
        self.variation = variation

    def set_std(self, std: List):
        """Method to set std"""
        self.std = std

    def set_student_criteria(self, student_criteria: List):
        """Method to set student criteria"""
        self.student_criteria = student_criteria

    def calculate_statistics(self):
        """Method to calculate statistics of the experiment"""
        self._calculator.calculate_statistics()

    def calculate_criteria(self):
        """Method to calculate the criteria of the experiment """
        self._calculator.calculate_student_criteria()

    def calculate_regression_coeffs(self) -> Dict:
        """Method to calculate the regression coefficients for the experiment"""
        return self._calculator.calculate_regression_coeffs()

    def get_student_table_value(self, df, probability=0.025):
        """Method to get the table value of the student criteria

        :param df: degree of freedom
        :param probability: probability of the distribution from the one side:
            0.025 -> 0.005 in common
        """
        return self._calculator.get_student_table_value(df, probability)
