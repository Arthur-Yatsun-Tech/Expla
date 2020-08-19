from abc import ABC

from core.experiment import Experiment
from utils import ControllersUtils, LayoutsUtils


class BaseLayout(ABC):
    experiment = Experiment()
    utils = LayoutsUtils(experiment)
    controllers = ControllersUtils(experiment)

    def build_layout(self):
        """Create widgets and manipulate them"""
        pass

    @staticmethod
    def compose_layout(*args):
        """Method to compose all resources into one layout"""
        pass
