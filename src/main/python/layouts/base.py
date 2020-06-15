from abc import ABC

from core.experiment import Experiment


class BaseLayout(ABC):
    experiment = Experiment()

    def build_main_layout(self):
        """Get widgets and manipulate them"""
        pass

    @staticmethod
    def makeup(*args):
        """Compare all resources into one layout"""
        pass
