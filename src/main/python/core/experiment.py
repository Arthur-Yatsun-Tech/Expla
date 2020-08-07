import collections
from typing import List, Optional

from pandas import DataFrame

from core.calculator import Calculator, Criteria


class Experiment:
    """The class to describe the experiment"""

    def __init__(self, factors: int = 9,
                 count_of_experiments: int = 3,
                 levels: int = 5,
                 experiment_data: Optional[List] = None,
                 experiment_table: Optional[collections.defaultdict] = None):
        """
        :param factors: number of the factors of the experiment `x` values
        :param count_of_experiments: number of the experiments_data `y` values
        :param levels: numbers of variations levels. possible values - [2, 3, 5]
        :param experiment_data: numeric data of the experiment according to the
                factors and count of the experiment
        :param experiment_table: experiment table
        """
        self.factors = factors
        self.count_of_experiments = count_of_experiments
        self.levels = levels

        # TODO: Only for test proposals, remove it
        self.factors = 4
        self.count_of_experiments = 2
        self.levels = 2

        if experiment_data is None:
            self.experiments_data = []

        if experiment_table is None:
            self.experiment_table = []

    @property
    def rows(self):
        return self.factors * 25 if self.levels == 5 and self.factors >= 5 else \
               self.levels ** self.factors

    def calculate_statistics(self) -> DataFrame:
        """Method to calculate statistics of the experiment"""

        return Calculator(self.experiments_data).calculate()

    # todo: make general criteria calculations
    def get_student_cirteria(self):
        df = self.count_of_experiments - 1
        return Criteria.get_student_table_value(df)
