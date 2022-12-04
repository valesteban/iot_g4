from PyQt5.QtWidgets import QFrame, QWidget, QLayout, QVBoxLayout, QStackedWidget, QPushButton, QComboBox
from PyQt5.QtCore import QStateMachine, QState, QFinalState, QSignalTransition, QTimer
from PyQt5 import QtCore, QtGui

from gui.all_events import LivePlotRemoveEvent, LivePlotAddEvent, LivePlotNoIDEvent, LivePlotPlottingEvent, LivePlotReadyEvent
from gui.transitions import LivePlotAddTransition, LivePlotRemoveTransition, LivePlotNoIDTransition, LivePlotPlottingTransition, LivePlotReadyTransition
from gui.rasp import Controller

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

class PlotButtonUI:
    def __init__(self, button_start: QPushButton) -> None:
        self.ui_button = button_start

        icon_play = QtGui.QIcon()
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.icon_play = icon_play

        icon_pause = QtGui.QIcon()
        icon_pause.addPixmap(QtGui.QPixmap(":/icon_pause/images/pause-button_red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_pause.addPixmap(QtGui.QPixmap(":/icon_pause/images/pause-button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon_pause.addPixmap(QtGui.QPixmap(":/icon_pause/images/pause-button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.icon_pause = icon_pause
         

    def set_start_button(self):
        self.ui_button.setIcon(self.icon_play)  
        
    def set_pause_button(self):
        self.ui_button.setIcon(self.icon_pause)

class VarSelectionUI:
    plot_vars = ["temperatura", "press", "hum", "co", "rms"]
    plot_vars.extend(["amp_"+coord for coord in ["x", "y", "z"]])
    plot_vars.extend(["frec_"+coord for coord in ["x", "y", "z"]])
    plot_vars.extend(["racc_"+coord for coord in ["x", "y", "z"]])
    plot_vars.extend(["rgyr_"+coord for coord in ["x", "y", "z"]])

    def __init__(self, var_combobox: QComboBox, left_arrow: QPushButton, right_arrow: QPushButton) -> None:
        self.combo_box = var_combobox
        self.left = left_arrow
        self.right = right_arrow

        self.left.setDisabled(False)
        self.right.setDisabled(False)

        self.combo_box.addItems(self.plot_vars)

    def select_prev(self):
        len_combo = self.combo_box.count()
        index = self.combo_box.currentIndex()
        new_index = (index - 1)%len_combo
        self.combo_box.setCurrentIndex(new_index)

    def select_next(self):
        len_combo = self.combo_box.count()
        index = self.combo_box.currentIndex()
        new_index = (index + 1)%len_combo
        self.combo_box.setCurrentIndex(new_index)


class LivePlot:
    update_time_ms = 1000
    def __init__(self, plot_id, plot_list: PlotListsMachine, plot_manager: "LivePlotManager", controller: "Controller") -> None:
        self.plot_id = plot_id
        self.plot_list = plot_list
        self.plot_manager = plot_manager
        self.controller = controller
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_tick)

        self.controller = Controller(lambda: None, lambda: None, lambda: ids, lambda: data)

        self.active_id:int = "None"
        self.active_var:str = ""

        self.ui_plot = live_plot.Ui_Form_live_plot()
        self.plot_frame = QFrame()
        self.ui_plot.setupUi(self.plot_frame)
        self.ui_plot.frame_live_plot_display.setMinimumSize(QtCore.QSize(150,150))

        self.ui_plot.comboBox_live_plot_var_select.currentTextChanged.connect(self.update_var)

        self.var_select = VarSelectionUI(
            self.ui_plot.comboBox_live_plot_var_select,
            self.ui_plot.pushButton_live_plot_left_var,
            self.ui_plot.pushButton_live_plot_right_var)


        self.plot_btn = PlotButtonUI(
            self.ui_plot.pushButton_bottom_stop_play
        )

        plt.ion()
        self.fig = plt.figure(facecolor='black')
        
        #plt.plot(x,y)

        #self.axes = plt.axes()
        self.axes = self.fig.add_subplot(111)
        #self.axes = self.fig.add_axes((0,0,1,1))
        self.axes.set_facecolor("black")

        current_y = self.get_values_vec()
        self.line, = self.axes.plot(np.arange(0,30,1), current_y, 'g-')
        #self.axes = Axes()

        canvas_layout = QVBoxLayout(self.ui_plot.frame_live_plot_display)
        self.canvas = MatplotlibCanvas(axes=self.axes, parent=self.ui_plot.frame_live_plot_display, layout=canvas_layout)
        canvas_layout.addWidget(self.canvas)
        #self.canvas = MatplotlibCanvas(axes=self.fig, parent=self.ui_plot.frame_live_plot_display, layout=canvas_layout)
    
        self.ui_plot.pushButton_remove.clicked.connect(self.remove_plot)

        self.ui_plot.comboBox_live_plot_id_select.activated.connect(self.update_active_esp_id)

    def set_machine(self):
        self.machine = QStateMachine()

        state_active = QState(self.machine)

        state_no_id = QState(state_active)
        state_ready = QState(state_active)
        state_plotting = QState(state_active)
        state_finished = QFinalState(self.machine)

        trans_noid_ready = LivePlotReadyTransition(state_no_id)
        trans_noid_ready.setTargetState(state_ready)

        trans_ready_noid = LivePlotNoIDTransition(state_ready)
        trans_ready_noid.setTargetState(state_no_id)

        trans_ready_plot = LivePlotPlottingTransition(state_ready)
        trans_ready_plot.setTargetState(state_plotting)

        trans_plot_ready = LivePlotReadyTransition(state_plotting)
        trans_plot_ready.setTargetState(state_ready)

        trans_finished = QSignalTransition(self.ui_plot.pushButton_remove.clicked, state_active)
        trans_finished.setTargetState(state_finished)

        self.machine.setInitialState(state_active)
        state_active.setInitialState(state_ready)
        self.machine.start()

        self.machine.entered.connect(self.refresh_available_ids)
        state_no_id.assignProperty(self.plot_btn.ui_button, "enabled", False)
        state_ready.assignProperty(self.plot_btn.ui_button, "enabled", True)
        state_ready.entered.connect(self.on_ready)
        state_plotting.entered.connect(self.on_plot)
        self.machine.finished.connect(lambda: self.timer.stop)

    def update_var(self, var_name):
        self.active_var = var_name 
        
    def on_plot(self):
        self.plot_btn.set_pause_button
        self.timer.start(self.update_time_ms)

    def on_ready(self):
        self.plot_btn.set_start_button
        self.timer.stop()

    def plot_tick(self):
        data_val = self.get_values_vec()
        self.line.set_ydata(data_val)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_active_esp_id(self):
        self.active_id = int(self.ui_plot.comboBox_live_plot_id_select.currentText())

    def remove_plot(self):
        self.plot_manager.live_plots.pop(self.plot_id)
        self.plot_list.machine.postEvent(LivePlotRemoveEvent(self.plot_frame))

    def refresh_available_ids(self):
        ids = self.controller.keys_get()
        self.ui_plot.comboBox_live_plot_id_select.clear()
        if ids:
            self.machine.postEvent(LivePlotReadyEvent())
            self.ui_plot.comboBox_live_plot_id_select.addItems(ids)
            index = self.ui_plot.comboBox_live_plot_id_select.find(str(self.active_id))
            self.ui_plot.comboBox_live_plot_id_select.setCurrentIndex(index)
            self.update_active_esp_id()
        else:
            self.machine.postEvent(LivePlotNoIDEvent())

    def get_values_vec(self):
        max_len = 30

        val_vec = np.zeros(max_len)
        all_id_tuples = self.controller.data_get(self.active_id)
        actual_len = 0
        ind = len(all_id_tuples)
        while (actual_len < max_len) and (ind >= 0):
            val = all_id_tuples[ind][1].get(self.active_var)
            if val:
                val_vec[actual_len] = val
                actual_len += 1
            ind -= 1 
        return val_vec

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
data = []
index = 0

if __name__ == "__main__":
    def apdeit_data():
        data.append(["3", {"temperature": np.sin(index)}])
        index += 0.01
    timer = QTimer()
    timer.timeout.connect()
    timer.start(500)
