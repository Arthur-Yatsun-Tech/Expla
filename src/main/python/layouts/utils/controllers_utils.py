from PySide2.QtWidgets import QGroupBox

from core.table_planner import TablePlanner
from layouts.utils.layouts_utils import LayoutsUtils


class ControllersUtils:
    """Class to handle all elements controllers"""

    def __init__(self, experiment):
        self.experiment = experiment
        self.utils = LayoutsUtils(experiment)

    def disable_experiments_cells_by_number_of_factors(self, parameters_layout: QGroupBox,
                                                       factors: int):
        """Method to disable cells in the experiments layout by the factor.
           Method is the controller of the QLineEdit for number of the factors

        :param parameters_layout: main parameters layout
        :param factors: number of the factors entered by the user
        """
        self.experiment.factors = self.utils.cast_parameter_to_int(factors)
        experiment_cells = self.utils.get_experiment_cells(parameters_layout)

        # todo: what is going on?
        x_cells = experiment_cells[:9][::-1]
        d1_cells = experiment_cells[9:18][::-1]
        d2_cells = experiment_cells[18:][::-1]

        if self.experiment.factors == 0:
            experiment_cells = list(set(experiment_cells) - set(d2_cells)) \
                if self.experiment.levels != 5 else experiment_cells
            list(map(
                lambda cell: self.utils.set_enabled(cell, True),
                experiment_cells))
        else:
            unused_cells = [
                *x_cells[:-self.experiment.factors],
                *d1_cells[:-self.experiment.factors],
                *d2_cells[:-self.experiment.factors]]
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                unused_cells))

    def disable_experiments_cells_by_variation_level(self,
                                                     variation_levels_layout: QGroupBox,
                                                     variation_level: int):
        """Method to disable cells in the experiments layout by the variation_level.
           Method is the controller of the QLineEdit for number of the factors

        :param variation_levels_layout: variation levels layout
        :param variation_level: variation level entered by the user
        """
        self.experiment.levels = self.utils.cast_parameter_to_int(variation_level)
        experiment_cells = self.utils.get_experiment_cells(variation_levels_layout)

        # todo: what is d2 cells?
        d2_cells = experiment_cells[18:]

        if self.experiment.levels != 5:
            list(map(
                lambda cell: self.utils.set_enabled(cell),
                d2_cells))
        else:
            if self.experiment.factors == 9:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells))
            else:
                list(map(
                    lambda cell: self.utils.set_enabled(cell, True),
                    d2_cells[:self.experiment.factors]))

    def set_number_of_experiments(self, experiment_series: int):
        """Method to set the number of experiments to the Experiment object.
           Method is the controller of the QLineEdit for the number of experiment series

        :param experiment_series: experiment series entered by the user
        """
        self.experiment.count_of_experiments = self.utils. \
            cast_parameter_to_int(experiment_series)

    def create_experiment_table_plan(self, controllers_layout: QGroupBox):
        """Method to create the experiment table plan

        :param controllers_layout: QGroupBox Object to get the table layout
            regarding its position
        """
        table = self.utils.get_experiment_table(controllers_layout)
        plan = TablePlanner(
            self.experiment.levels, self.experiment.factors).create_table()

        self.utils.set_experiment_plan(table, plan)

    def calculate(self, controllers_layout: QGroupBox):
        """Method to make all calculations

        :param controllers_layout: QGroup Object to manipulate with another layouts
        """
        experiment_table = self.utils.get_experiment_table(controllers_layout)
        self.utils.get_experiments_data(experiment_table)

        self.experiment.calculate_statistics()
        self.experiment.calculate_criteria()
        self.utils.set_statistics_data_in_table(experiment_table)

        # TODO: refactor set_criteria method
        self.utils.set_criteria_in_table(
            controllers_layout, self.experiment.max_student_value)

        regression_table = self.utils.get_regression_table(controllers_layout)
        self.experiment.calculate_regression_coeffs()
        self.utils.set_regression_coeffs_in_table(regression_table)
