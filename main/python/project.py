from table_planning.table_planer import TablePlanner


class Project:
    def __init__(self, levels_count=0, factors_count=0, experiments_count=0):
        self.factors_count = factors_count
        self.levels_count = levels_count
        self.experiments_count = experiments_count

        def create_table(self):
            if self.levels_count and self.factors_count:
                self.table = TablePlanner(self.levels_count, self.factors_count)
