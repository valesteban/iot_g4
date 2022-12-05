from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtCore import QStateMachine, QState, QSignalTransition, QThread

from gui.all_events import EndFindEvent, ESPFoundEvent
from gui.forms import main_display
from gui.live_plot import LivePlotManager
from gui.transitions import EndFindTransition, ESPFoundTransition
from gui.esp_lists import ListsMachine
from gui.esp_dev import ESPDicts
from gui.workers import FindESPWorker


class Controller:
    def __init__(self, db_config_set, db_config_get, db_get_ids, db_get_data, ble_controller_cls) -> None:
        self.set_methods(db_config_set, db_config_get, db_get_ids, db_get_data, ble_controller_cls)

    def set_methods(self, db_config_set, db_config_get, db_get_ids, db_get_data, ble_controller_cls):
        self.config_set = db_config_set
        self.config_get = db_config_get
        self.keys_get = db_get_ids
        self.data_get = db_get_data
        self.ble_controller =ble_controller_cls

class DeviceSearch:
    def __init__(self, main_disp: main_display.Ui_MainWindow, esp_dict_list: ESPDicts, controller: Controller) -> None:
        self.main_disp = main_disp
        self.esp_dict_list = esp_dict_list
        self.controller = controller

        self.gui_controller = self.controller.ble_controller(self)
        self.worker = FindESPWorker(self.main_disp.centralwidget, self, self.gui_controller.actualizarMacs)

        self.machine = QStateMachine()
        state_buscando = QState(self.machine)
        state_sin_buscar = QState(self.machine)
        
        trans_no_a_buscar = QSignalTransition(self.main_disp.pushButton_search_refresh.clicked, state_sin_buscar)
        trans_no_a_buscar.setTargetState(state_buscando)
        trans_no_a_buscar.triggered.connect(self.perform_search)
        #state_sin_buscar.addTransition(self.main_disp.pushButton_search_refresh.clicked, state_buscando)
    
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

    def perform_search(self):
        thread = QThread()
        #worker.moveToThread(thread)
        #thread.started.connect(worker.process)
        #worker.finished.connect(thread.quit)
        #worker.finished.connect(worker.deleteLater)
        #thread.finished.connect(thread.deleteLater)
        self.worker.setup_thread(thread)
        # necesario hacer self. para que quede una referencia a los objetos y no se maten solos :(
        self.thread = thread
        self.worker = self.worker
        thread.start()

    def notify_esp_found(self, esp_id: str, esp_mac: str):
        self.machine.postEvent(ESPFoundEvent(esp_id, esp_mac))

    def notify_end_find(self):
        self.machine.postEvent(EndFindEvent())

class Rasp:
    def __init__(self, window: QMainWindow, controller: Controller) -> None:
        self.window = window
        self.ui_main_disp = main_display.Ui_MainWindow()
        self.ui_main_disp.setupUi(self.window)
        self.controller = controller

        self.plot_manager = LivePlotManager(self.ui_main_disp, controller)

        self.esp_disp_list = ListsMachine(
            self.ui_main_disp.scrollAreaWidgetContents_found_area, 
            self.ui_main_disp.verticalLayout_found_list,
            self.ui_main_disp.scrollAreaWidgetContents_active_esp,
            self.ui_main_disp.verticalLayout_active_list)
        
        self.esp_dict_list = ESPDicts(self.esp_disp_list, self.window, controller)

        self.device_search = DeviceSearch(self.ui_main_disp, self.esp_dict_list, controller)