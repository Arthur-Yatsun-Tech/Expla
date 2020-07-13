from PySide2.QtWidgets import QTabWidget, QWidget
from dataclasses import dataclass

from layouts import BaseLayout
from layouts.tabs_layouts import TableLayout, CriteriaLayout

TABLE_TITLE = 'Таблица эксперемента'
CRITERIA_TITLE = 'Критерии'
REGRESSION_COEFS_TITLE = 'Коэфициенты регрессии'
PLOTS_TITLE = 'Графики'
REGRESSION_EQUATION_TITLE = 'Регрессионное уравнение'


@dataclass
class Tabs:
    main_tab: QTabWidget
    regression_coefs_tab: QWidget
    plots_tab: QWidget
    regression_equation_tab: QWidget


class BaseTabLayout(BaseLayout):
    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        tabs = self.utils.get_elements(Tabs)

        return self.compose_layout(tabs)

    @staticmethod
    def compose_layout(tabs):
        table_tab = TableLayout().main_layout
        criteria_tab = CriteriaLayout().main_layout

        tabs.main_tab.addTab(table_tab, TABLE_TITLE)
        tabs.main_tab.addTab(criteria_tab, CRITERIA_TITLE)
        tabs.main_tab.addTab(tabs.regression_coefs_tab, REGRESSION_COEFS_TITLE)
        tabs.main_tab.addTab(tabs.plots_tab, PLOTS_TITLE)
        tabs.main_tab.addTab(tabs.regression_equation_tab, REGRESSION_EQUATION_TITLE)

        return tabs.main_tab
