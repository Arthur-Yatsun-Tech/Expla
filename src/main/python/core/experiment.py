from core.criteria import Criteria
from core.statistics import Statistics


class Experiment:
    def __init__(self):
        self.factors = 9
        self.count_of_experiments = 3
        self.levels = 5
        self.experiments_data = []
        """
        factors: count of experiment factors
        experiments: count of experiment series
        levels: count of variation levels
        """

    @property
    def rows(self):
        return self.factors * 25 if self.levels == 5 and self.factors >= 5 else \
               self.levels ** self.factors

    def calculate_statistics(self):
        return Statistics(self.experiments_data).calculate()

    def get_student_cirteria(self):
        df = self.count_of_experiments - 1
        return Criteria.get_student_table_value(df)
