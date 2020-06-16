from abc import ABC

from core.experiment import Experiment
from layouts.controllers import Controllers
from layouts.utils import Utils


class BaseLayout(ABC):
    experiment = Experiment()
    utils = Utils()
    controllers = Controllers()

    def build_main_layout(self):
        """Get widgets and manipulate them"""
        pass

    @staticmethod
    def makeup(*args):
        """Compare all resources into one layout"""
        pass
