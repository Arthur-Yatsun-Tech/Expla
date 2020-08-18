from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QScrollArea, QWidget
from dataclasses import dataclass
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from layouts import BaseLayout


@dataclass
class PlotsLayouts:
    plot1_layout: QVBoxLayout
    plot2_layout: QVBoxLayout
    plot3_layout: QVBoxLayout
    plot4_layout: QVBoxLayout
    plot5_layout: QVBoxLayout


@dataclass
class Layouts:
    main_inner_layout: QVBoxLayout
    main_layout: QWidget


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotsLayout(BaseLayout):
    """Layout to display the experiment plots"""

    def __init__(self):
        self.main_layout = self.build_layout()

    def build_layout(self):
        layouts = self.utils.get_elements(Layouts)
        plots_layouts = self.utils.get_elements(PlotsLayouts)
        plots = self.create_plots()

        return self.compose_layout(layouts, plots_layouts, plots)

    @staticmethod
    def compose_layout(layouts, plots_layouts, plots):
        plots_layouts.plot1_layout.addWidget(plots[0])
        plots_layouts.plot2_layout.addWidget(plots[1])
        plots_layouts.plot3_layout.addWidget(plots[2])
        plots_layouts.plot4_layout.addWidget(plots[3])
        plots_layouts.plot5_layout.addWidget(plots[4])

        # layouts.main_inner_layout.setWidgetResizable(True)
        layouts.main_inner_layout.addLayout(plots_layouts.plot1_layout)
        layouts.main_inner_layout.addLayout(plots_layouts.plot2_layout)
        layouts.main_inner_layout.addLayout(plots_layouts.plot3_layout)
        layouts.main_inner_layout.addLayout(plots_layouts.plot4_layout)
        layouts.main_inner_layout.addLayout(plots_layouts.plot5_layout)

        layouts.main_layout.setLayout(layouts.main_inner_layout)
        mw = QScrollArea()
        mw.setWidget(layouts.main_layout)
        return mw

    def create_plots(self):
        plots = []
        for i in range(5):
            sc = MplCanvas(self)
            sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
            plots.append(sc)
        return plots
