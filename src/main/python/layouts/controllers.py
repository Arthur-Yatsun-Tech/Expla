from PySide2.QtWidgets import QGroupBox

from core.experiment import Experiment
from core.table_planer import TablePlanner
from layouts.utils import Utils


class Controllers:
    def __init__(self):
        self.utils = Utils()

    def disable_experiments_cells_by_factor(self, current_layout: QGroupBox, experiment: Experiment, factors: int):
        experiment.factors = self.utils.cast_parameter_to_int(factors)
        print(experiment.factors)

        experiment_cells = self.utils.get_experiment_cells(current_layout)

        x_cells = experiment_cells[:9][::-1]
        d1_cells = experiment_cells[9:18][::-1]
        d2_cells = experiment_cells[18:][::-1]

        if experiment.factors == 0:

            experiment_cells = list(set(experiment_cells) - set(d2_cells)) if experiment.levels != 5 else \
                               experiment_cells
            list(map(
                lambda cell: self.utils.set_enabled(cell, True),
                experiment_cells))
        else:
            unused_cells = [
                *x_cells[:-experiment.factors],
                *d1_cells[:-experiment.factors],
                *d2_cells[:-experiment.factors]]
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                unused_cells))

    def disable_experiments_cells_by_level(self, current_layout, experiment, level):
        experiment.levels = self.utils.cast_parameter_to_int(level)

        experiment_cells = self.utils.get_experiment_cells(current_layout)
        d2_cells = experiment_cells[18:]

        if experiment.levels != 5:
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                d2_cells))
        else:
            if experiment.factors == 9:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells))
            else:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells[:experiment.factors]))

    def set_count_of_experiments(self, experiment, count_of_experiments):
        experiment.count_of_experiments = self.utils.cast_parameter_to_int(count_of_experiments)

    def init_experiment_table_plan(self, current_layout, experiment):
        table = self.utils.get_experiment_table(current_layout)

        plan = TablePlanner(experiment.levels, experiment.factors).create_table()
        self.utils.set_experiment_plan(experiment, table, plan)

    def calculate(self, current_layout, experiment):
        table = self.utils.get_experiment_table(current_layout)
        self.utils.get_experiments_data(experiment, table)

        statistics = experiment.calculate_statistics()
        self.utils.set_statistics(table, experiment, statistics)

        self.utils.set_criteria(current_layout, experiment, max(statistics['t']))

