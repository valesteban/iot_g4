from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtCore import QStateMachine, QState

from gui.forms import main_display
from gui.live_plot import LivePlotManager
from gui.transitions import EndFindTransition, ESPFoundTransition
from gui.esp_lists import ListsMachine
from gui.esp_dev import ESPDicts

class DeviceSearch:
    def __init__(self, main_disp: main_display.Ui_MainWindow, esp_dict_list: ESPDicts) -> None:
        self.main_disp = main_disp
        self.esp_dict_list = esp_dict_list

        self.machine = QStateMachine()
        state_buscando = QState(self.machine)
        state_sin_buscar = QState(self.machine)
        
        state_sin_buscar.addTransition(self.main_disp.pushButton_search_refresh.clicked, state_buscando)
    
        endfind_transition = EndFindTransition()
        endfind_transition.setTargetState(state_sin_buscar)
        state_buscando.addTransition(endfind_transition)

        state_buscando.assignProperty(self.main_disp.pushButton_search_refresh, "enabled", False)
        state_sin_buscar.assignProperty(self.main_disp.pushButton_search_refresh, "enabled", True)

        self.machine.setInitialState(state_sin_buscar)

        found_trans = ESPFoundTransition(self.esp_dict_list)
        state_buscando.addTransition(found_trans)
        found_trans.triggered.connect(found_trans.transition_slot)

        self.machine.start()



class Rasp:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.ui_main_disp = main_display.Ui_MainWindow()
        self.ui_main_disp.setupUi(self.window)

        self.plot_manager = LivePlotManager(self.ui_main_disp)

        self.esp_disp_list = ListsMachine(
            self.ui_main_disp.scrollAreaWidgetContents_found_area, 
            self.ui_main_disp.verticalLayout_found_list,
            self.ui_main_disp.scrollAreaWidgetContents_active_esp,
            self.ui_main_disp.verticalLayout_active_list)
        
        self.esp_dict_list = ESPDicts(self.esp_disp_list, self.window)

        self.device_search = DeviceSearch(self.ui_main_disp, self.esp_dict_list)