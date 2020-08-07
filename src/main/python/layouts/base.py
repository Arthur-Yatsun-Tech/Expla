from abc import ABC

from core.experiment import Experiment
from layouts.utils import Utils, ControllersUtils


class BaseLayout(ABC):
    experiment = Experiment()
    utils = Utils()
    controllers = ControllersUtils()

    def build_layout(self):
        """Create widgets and manipulate them"""
        pass

    @staticmethod
    def compose_layout(*args):
        """Method to compose all resources into one layout"""
        pass
