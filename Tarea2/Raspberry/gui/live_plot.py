from PyQt5.QtWidgets import QFrame, QWidget, QLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import QStateMachine, QState
from PyQt5 import QtCore

from gui.all_events import LivePlotRemoveEvent, LivePlotAddEvent
from gui.transitions import LivePlotAddTransition, LivePlotRemoveTransition

from gui.forms import main_display, live_plot

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.legend import _get_legend_handles_labels
import numpy as np


class PlotListsMachine:
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, filled_page: QStackedWidget) -> None:
        self.num_plots  = 0
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout
        self.page_filled = filled_page

        self.machine = QStateMachine()

        state_plot_empty = QState(self.machine)
        state_plot_filled = QState(self.machine)

        state_plot_empty.assignProperty(self.page_filled, "currentIndex", 1)
        state_plot_filled.assignProperty(self.page_filled, "currentIndex", 0)

        # transitions

        trans_plot_empty_to_filled = LivePlotAddTransition(self, self.widget_list_parent, self.list_layout)
        trans_plot_empty_to_filled.setTargetState(state_plot_filled)
        state_plot_empty.addTransition(trans_plot_empty_to_filled)

        trans_filled_to_filled = LivePlotAddTransition(self, self.widget_list_parent, self.list_layout)
        state_plot_filled.addTransition(trans_filled_to_filled)

        trans_plot_filled_to_empty = LivePlotRemoveTransition(self, self.widget_list_parent, self.list_layout)
        trans_plot_filled_to_empty.setTargetState(state_plot_empty)
        state_plot_filled.addTransition(trans_plot_filled_to_empty)

        self.machine.setInitialState(state_plot_empty)
        self.machine.start()

class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, axes: Axes, parent=None, layout=None, width=5, height=4, dpi=120):
        self.axes = axes
        self.parent = parent
        self.layout: QVBoxLayout = layout
        self.toolbar: NavigationToolbar = None
        super(MatplotlibCanvas, self).__init__(axes.figure)
        axes.figure.tight_layout()

        handles, labels = _get_legend_handles_labels([axes], dict())
        if handles:
        #if True:
            legend = self.axes.legend()
            legend.set_draggable(True)

        #self.set_toolbar()

    def set_toolbar(self):

        rcParams['toolbar'] = 'None'
        my_toolitems = NavigationToolbar.toolitems.copy()
        remove_these = ["Subplots", "Save"]
        for i in range(len(my_toolitems)-1,-1,-1):
            item_first_name = my_toolitems[i][0]
            if item_first_name in remove_these:
                my_toolitems.pop(i)

        NavigationToolbar.toolitems = my_toolitems
        self.toolbar = NavigationToolbar(self, self.parent)
        #canv = self.axes.figure.canvas
        #canv.manager.toolmanager.remove_tool("subplots")
        # IMPORTANT: don't use "if self.layout: ", for some reason, bool(self.layout) is False
        if self.layout is not None:
            self.layout.addWidget(self.toolbar)

class LivePlot:
    def __init__(self, plot_id, plot_list: PlotListsMachine, plot_manager: "LivePlotManager", controller: "Controller") -> None:
        self.plot_id = plot_id
        self.plot_list = plot_list
        self.plot_manager = plot_manager

        self.ui_plot = live_plot.Ui_Form_live_plot()
        self.plot_frame = QFrame()
        self.ui_plot.setupUi(self.plot_frame)
        self.ui_plot.frame_live_plot_display.setMinimumSize(QtCore.QSize(150,150))

        self.fig = plt.figure(facecolor='black')

        #plt.plot(x,y)

        #self.axes = plt.axes()

        self.axes = self.fig.add_axes((0,0,1,1))
        self.axes.set_facecolor("black")

        #self.axes.plot([1,2,3,4],[4,1,3,2])
        #self.axes = Axes()

        canvas_layout = QVBoxLayout(self.ui_plot.frame_live_plot_display)
        self.canvas = MatplotlibCanvas(axes=self.axes, parent=self.ui_plot.frame_live_plot_display, layout=canvas_layout)
        canvas_layout.addWidget(self.canvas)
        #self.canvas = MatplotlibCanvas(axes=self.fig, parent=self.ui_plot.frame_live_plot_display, layout=canvas_layout)


        self.ui_plot.pushButton_remove.clicked.connect(self.remove_plot)

    def remove_plot(self):
        self.plot_manager.live_plots.pop(self.plot_id)
        self.plot_list.machine.postEvent(LivePlotRemoveEvent(self.plot_frame))

    def refresh_available_ids(self):
        self.ui_plot.comboBox_live_plot_id_select.clear()
        self.ui_plot.comboBox_live_plot_id_select.addItems


class LivePlotManager:
    def __init__(self, ui_main: main_display.Ui_MainWindow) -> None:
        self.plot_list = PlotListsMachine(
            ui_main.scrollAreaWidgetContents_added_plots, 
            ui_main.verticalLayout_added_plots_list,
            ui_main.stackedWidget_plot_count)
        self.ui_main = ui_main
        self.live_plots = dict()

        ui_main.pushButton_add_live_plot.clicked.connect(self.add_new_plot)

    def add_new_plot(self):
        new_plot = LivePlot(self.plot_list.num_plots, self.plot_list, self)
        self.live_plots[self.plot_list.num_plots] = new_plot
        self.plot_list.machine.postEvent(LivePlotAddEvent(new_plot.plot_frame))

ids = ["3", "4"]

