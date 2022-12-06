from PyQt5.QtCore import QStateMachine, QState, QFinalState, QSignalTransition, QThread

from PyQt5.QtWidgets import QFrame, QDialog, QPushButton
from multiprocessing import Lock

import ipaddress
import sys

from gui.all_events import CheckNoWifiEvent, ValidWifiConfigEvent, InvalidWifiConfigEvent, InactiveESPEvent, AbleToSendEvent, UnableToSendEvent, SendStartEvent, ESPActiveEvent, ESPRemoveActiveEvent, ESPAddActiveEvent, ESPRemoveFoundEvent, ESPAddFoundEvent, ESPFoundEvent, ESPSendingEvent
from gui.states import WifiState, NoWifiState, FoundState
from gui.transitions import InactiveESPTransition, CheckNoWifiTransition, AbleToSendTransition, UnableToSendTransition, ValidWifiConfigTransition, InvalidWifiConfigTransition, StartClickTransition, ESPActiveTransition, ESPFoundTransition, SendStartTransition, ESPSendingTransition, ESPSleepingTransition
from gui.esp_lists import ListsMachine
from gui.properties import WifiProperties, ConfigProperties
from gui.wifi_ui import WifiDisplay
from gui.config_ui import StatusConfigUI
from gui.active_ui import StartButtonUI, SendStatusUI, ESPInfo
from gui.workers import ConfigESPBLEWorker, ConfigESPWifiWorker

from gui.forms import esp_found_item, esp_active_item,  esp_wifi_config, esp_config_win


class ESPDicts:
    def __init__(self, esp_lists_machine, main_win, controller: "Controller") -> None:
        self.mutex = Lock()
        self.esp_lists_machine = esp_lists_machine
        self.main_win = main_win
        self.controller = controller

        self.esp_dict = dict()

    def check_esp(self, esp_id, esp_mac):
        try:
            self.mutex.acquire()
            if esp_id not in self.esp_dict.keys():
                self.esp_dict[esp_id] = ESPDevice(esp_id, esp_mac, self.esp_lists_machine, self, self.main_win, self.controller)
                self.esp_dict[esp_id].set_machine()
            else:
                self.esp_dict[esp_id].machine.postEvent(ESPFoundEvent(esp_id, esp_mac))
        finally:
            self.mutex.release()

    def remove_esp(self, esp_id) -> None:
        try:
            self.mutex.acquire()
            if esp_id in self.esp_dict.keys():
                self.esp_dict.pop(esp_id)
        finally:
            self.mutex.release()


class ESPConfig:
    def __init__(self, esp: "ESPDevice") -> None:
        self.esp = esp
        self.machine: QStateMachine = None

        self.wifi_properties = WifiProperties()
        self.wifi_ui = WifiDisplay(self.esp.ui_wifi, self.wifi_properties)

        self.config_wifi = None
        self.send_wifi = False

        self.status_properties = ConfigProperties()
        self.status_ui = StatusConfigUI(self.esp.ui_config_win, self.esp.ui_wifi, self.status_properties)

    def set_medium_and_post(self, config_wifi: bool=None, send_wifi:bool=None):
        if config_wifi is not None:
            self.config_wifi = config_wifi
        if send_wifi is not None:
            self.send_wifi = send_wifi
        self.machine.postEvent(CheckNoWifiEvent(self.config_wifi, self.send_wifi))

    def _on_finish(self):
        print("Config finished!")

    def set_machine(self) ->None:
        self.machine = QStateMachine()
        state_config_paralell = QState(childMode=QState.ChildMode.ParallelStates, parent=self.machine) 
        state_finished = QFinalState(self.machine)

        state_configs = QState(state_config_paralell)
        state_can_send = QState(state_config_paralell)

        state_no_config = QState(state_configs)
        state_config_wifi = WifiState(state_configs)
        state_config_no_wifi = NoWifiState(state_configs)
        state_wifi_error = QState(state_configs)

        state_unable_to_send = QState(state_can_send)
        state_able_to_send = QState(state_can_send)

        state_configs.setInitialState(state_no_config)
        state_can_send.setInitialState(state_unable_to_send)

        self.machine.setInitialState(state_config_paralell)
        
        trans_finished = InactiveESPTransition()
        trans_finished.setTargetState(state_finished)
        state_config_paralell.addTransition(trans_finished)

        self.machine.finished.connect(self._on_finish)

        state_no_config.entered.connect(self._enter_no_config)

        def _activate_wifi_config_check():
            self.wifi_ui.set_invalid_signal_slots()
            self.wifi_ui.set_valid_signal_slots()

        state_no_config.exited.connect(_activate_wifi_config_check)

        self.esp.ui_active.pushButton_config_medium_bluetooth.clicked.connect(lambda: self.set_medium_and_post(config_wifi=False))
        self.esp.ui_active.pushButton_config_medium_bd.clicked.connect(lambda: self.set_medium_and_post(config_wifi=True))
        self.esp.ui_config_win.pushButton_send_bluetooth.clicked.connect(lambda: self.set_medium_and_post(send_wifi=False))
        self.esp.ui_config_win.pushButton_send_wifi.clicked.connect(lambda: self.set_medium_and_post(send_wifi=True))

        # la idea es abrir la ventana de configuración cuando la rasp no ha sido previamente configurada
        trans_no_config_to_bluetooth = QSignalTransition(self.esp.ui_active.pushButton_config_medium_bluetooth.clicked, state_no_config)
        trans_no_config_to_bluetooth.setTargetState(state_config_no_wifi)
        trans_no_config_to_bluetooth.triggered.connect(self.esp.open_config_dialog)

        trans_no_config_to_wifi = QSignalTransition(self.esp.ui_active.pushButton_config_medium_bd.clicked, state_no_config)
        trans_no_config_to_wifi.setTargetState(state_config_wifi)
        trans_no_config_to_wifi.triggered.connect(self.esp.open_config_dialog)

        #state_no_config.exited.connect(self.esp.open_config_dialog)
        #state_no_config.addTransition(self.esp.ui_active.pushButton_config_medium_bluetooth.clicked, state_config_no_wifi)
        #state_no_config.addTransition(self.esp.ui_active.pushButton_config_medium_bd.clicked, state_config_wifi)

        state_no_config.addTransition(self.esp.ui_config_win.pushButton_send_bluetooth.clicked, state_config_no_wifi)
        state_no_config.addTransition(self.esp.ui_config_win.pushButton_send_wifi.clicked, state_config_wifi)

        state_config_no_wifi.addTransition(self.esp.ui_active.pushButton_config_medium_bd.clicked, state_config_wifi)
        state_config_no_wifi.addTransition(self.esp.ui_config_win.pushButton_send_wifi.clicked, state_config_wifi)

        trans_wifi = CheckNoWifiTransition()
        trans_wifi.setTargetState(state_config_no_wifi)
        state_config_wifi.addTransition(trans_wifi)

        state_no_config.assignProperty(self.esp.ui_active.toolButton_esp_active_wifi_config, "enabled", False)
        state_config_no_wifi.assignProperty(self.esp.ui_active.toolButton_esp_active_wifi_config, "enabled", False)
        state_config_wifi.assignProperty(self.esp.ui_active.toolButton_esp_active_wifi_config, "enabled", True)

        state_unable_to_send.assignProperty(self.esp.ui_active.pushButton_esp_active_restart, "enabled", False)
        state_able_to_send.assignProperty(self.esp.ui_active.pushButton_esp_active_restart, "enabled", True)

        trans_unable_to_able = AbleToSendTransition()
        trans_unable_to_able.setTargetState(state_able_to_send)
        state_unable_to_send.addTransition(trans_unable_to_able)

        trans_able_to_unable = UnableToSendTransition()
        trans_able_to_unable.setTargetState(state_unable_to_send)
        state_able_to_send.addTransition(trans_able_to_unable)

        #state_no_config.entered.connect(lambda: self.esp.ui_active.toolButton_esp_active_wifi_config.hideContent())

        def _auto_hide_toolbar():
            if self.esp.ui_active.toolButton_esp_active_wifi_config.isChecked():
                self.esp.ui_active.toolButton_esp_active_wifi_config.hideContent()
                self.esp.ui_active.toolButton_esp_active_wifi_config.setChecked(False)


        def _auto_show_toolbar():
            if not self.esp.ui_active.toolButton_esp_active_wifi_config.isChecked():
                self.esp.ui_active.toolButton_esp_active_wifi_config.click()

        state_config_wifi.entered.connect(_auto_show_toolbar)
        state_config_no_wifi.entered.connect(_auto_hide_toolbar)

        state_config_wifi.entered.connect(self._enter_wifi)
        state_config_no_wifi.entered.connect(self._enter_no_wifi)
        
        trans_wifi_to_error = InvalidWifiConfigTransition()
        trans_wifi_to_error.setTargetState(state_wifi_error)
        state_config_wifi.addTransition(trans_wifi_to_error)

        trans_wifi_to_error.triggered.connect(lambda: print("uwu"))

        for signal in self.wifi_ui.get_signals():
            trans_wifi_error = QSignalTransition(signal)
            trans_wifi_error.setTargetState(state_wifi_error)
            state_wifi_error.addTransition(trans_wifi_error)

        trans_error_to_wifi = ValidWifiConfigTransition()
        trans_error_to_wifi.setTargetState(state_config_wifi)
        state_wifi_error.addTransition(trans_error_to_wifi)
        state_wifi_error.entered.connect(lambda: self.machine.postEvent(UnableToSendEvent()))

        def _check_valid_wifi():
            print("checking stuff")
            result = self.wifi_properties.validate_all(*self.wifi_ui.get_all_ui_values())
            self.wifi_properties.set_all(*self.wifi_ui.get_all_ui_values())
            if result:
                self.machine.postEvent(ValidWifiConfigEvent())
                self.machine.postEvent(AbleToSendEvent())

        state_wifi_error.entered.connect(_check_valid_wifi)

        trans_send_clicked_wifi = StartClickTransition(self, self.esp.ui_active.pushButton_esp_active_restart.clicked)
        state_config_wifi.addTransition(trans_send_clicked_wifi)

        trans_send_clicked_nowifi = StartClickTransition(self, self.esp.ui_active.pushButton_esp_active_restart.clicked)
        state_config_no_wifi.addTransition(trans_send_clicked_nowifi)

        self.machine.start()

    def _check_valid_connections(self):
        if self.config_wifi is None or self.send_wifi is None:
            self.machine.postEvent(UnableToSendEvent())
        else:
            self.machine.postEvent(AbleToSendEvent())

    def _enter_no_config(self):
        self.wifi_ui.set_ui_to_default_view()
        self._load_config_from_model()
        self.wifi_ui.load_from_properties_into_ui()
    
    def _enter_no_wifi(self):
        self._check_valid_connections()
        self.esp.worker_slot = self.esp.perform_ble_config

    def _enter_wifi(self):
        self._check_valid_connections()
        self.esp.worker_slot = self.esp.perform_wifi_config

    def _load_config_from_model(self):
        print(self.esp.esp_id)
        
        res = self.esp.controller.config_get(self.esp.esp_id)
        print(res)

        if res:
            res = res[0]
            print(ipaddress.IPv4Address(res[10]))
            host_ipv4 = str(ipaddress.IPv4Address(res[10]))
            bd_wifi_conf = (host_ipv4, res[8], res[9], res[11], res[12])
            bd_status_conf = (res[1], res[2], res[7], res[3], res[4], res[5], res[6])

            self.wifi_properties.set_all(*bd_wifi_conf)
            self.status_properties.set_all(*bd_status_conf)

    def _save_config_into_model(self):
        self.wifi_properties.reset_invalid()
        self.status_properties.reset_invalid()

        wifi_conf = self.wifi_properties.get_all()
        status_conf = self.status_properties.get_all()

        wifi_keys = WifiProperties.attrs
        status_keys = ConfigProperties.attrs

        print("id esp:", self.esp.esp_id)

        host_ipv4 = ipaddress.IPv4Address(wifi_conf[0])
        new_ = {
            "id_device": self.esp.esp_id,
            "discontinuos_time": status_conf[3],
            "host_ip_addr": host_ipv4,
            "tcp_port": wifi_conf[1],
            "udp_port": wifi_conf[2],
            "host_ip_addr": str(host_ipv4),
            "pass": wifi_conf[4] 
        }
        
        [new_.__setitem__(status_keys[i],status_conf[i]) for i in range(2)]
        [new_.__setitem__(status_keys[i],status_conf[i]) for i in range(3,7)]
        new_[wifi_keys[3]] = wifi_conf[3]

        print(new_)


        try:
            self.esp.controller.config_set(new_)
        except Exception as e:
            print("Falló la escritura en el DB *jabalí explotando*")
            print(e, file= sys.stderr)
            raise(e)

class ESPDevice:
    def __init__(self, esp_id, esp_mac, esp_lists_machine: ListsMachine, esp_dict_list: "ESPDicts", main_win, controller: "Controller") -> None:
        self.esp_id = esp_id
        self.esp_mac = esp_mac
        self.machine: QStateMachine = None
        self.esp_lists_machine: ListsMachine = esp_lists_machine
        self.esp_dict = esp_dict_list
        self.main_win = main_win
        self.controller = controller
        self.gui_controller = self.controller.ble_controller(self.controller.rasp_, self)

        self.worker_slot = self.perform_ble_config

        self.ui_found: esp_found_item.Ui_Form_esp_found_item = None

        self.found_widget: QFrame = None
        self.set_found_widget()
        self.found_widget.setVisible(False)

        self.add_btn: QPushButton = None
        self.ui_active: esp_active_item.Ui_Form_esp_active = None
        self.ui_wifi: esp_wifi_config.Ui_Form_wifi_config = None

        self.ui_config_dialog = QDialog(self.main_win)
        self.ui_config_win: esp_config_win.Ui_Dialog_esp_config = esp_config_win.Ui_Dialog_esp_config()
        self.ui_config_win.setupUi(self.ui_config_dialog)

        self.config: ESPConfig = None
        self.active_widget: QFrame = None
        self.set_active_widget()
        self.active_widget.setVisible(False)

        self.start_btn = StartButtonUI(self.ui_active.pushButton_esp_active_restart)
        self.send_status = SendStatusUI(
            self.ui_active.label_esp_active_status_icon, 
            self.ui_active.label_esp_active_status_edit)

        self.esp_info_found = ESPInfo(
            self.ui_found.label_esp_found_id_edit,
            self.ui_found.label_esp_found_mac_edit
        )

        self.esp_info_active = ESPInfo(
            self.ui_active.label_esp_active_id_edit,
            self.ui_active.label_esp_active_mac_edit
        )

        self.esp_info_found.set_id(self.esp_id, self.esp_mac)
        self.esp_info_active.set_id(self.esp_id, self.esp_mac)
      

    def set_machine(self) -> None:
        self.machine = QStateMachine()
        state_encontrado = FoundState(self, self.machine)
        state_activo = QState(self.machine)
        state_dead = QState(self.machine)
        state_proceso_envio = QState(self.machine)
        state_finished = QFinalState(self.machine)
 
        state_configurando = QState(state_proceso_envio)
        state_envio = QState(state_proceso_envio)
        state_mimir = QState(state_proceso_envio)
 
        self.machine.finished.connect(self._on_finish)
        #state_encontrado.addTransition(_found_to_active_slot, state_activo)

        for source_state in [state_encontrado, state_activo, state_dead]:

            trans_make_inactive = InactiveESPTransition()
            trans_make_inactive.setTargetState(state_finished)
            source_state.addTransition(trans_make_inactive)

        trans_found_to_active = ESPActiveTransition()
        trans_found_to_active.setTargetState(state_activo)
        state_encontrado.addTransition(trans_found_to_active)

        trans_make_active = ESPFoundTransition(self.esp_dict)
        trans_make_active.setTargetState(state_activo)
        state_dead.addTransition(trans_make_active)

        trans_begin_send = SendStartTransition()
        trans_begin_send.setTargetState(state_proceso_envio)
        state_activo.addTransition(trans_begin_send)

        state_proceso_envio.entered.connect(lambda:
            self.send_status.set_send_parameters(
                self.config.config_wifi,
                self.config.send_wifi,
                self.config.status_ui.actual_status.name,
                self.ui_config_win.comboBox_protocol.currentText()
            ))


        trans_conf_to_send = ESPSendingTransition(state_configurando)
        trans_conf_to_send.setTargetState(state_envio)

        trans_send_to_sleep = ESPSleepingTransition(state_envio)
        trans_send_to_sleep.setTargetState(state_mimir)

        trans_sleep_to_send = ESPSendingTransition(state_mimir)
        trans_sleep_to_send.setTargetState(state_envio)

        trans_stop_config = ESPActiveTransition(state_configurando)
        trans_stop_config.setTargetState(state_activo)

        trans_stop_send = ESPActiveTransition(state_envio)
        trans_stop_send.setTargetState(state_activo)

        trans_stop_sleep = ESPActiveTransition(state_mimir)
        trans_stop_sleep.setTargetState(state_activo)

        state_proceso_envio.entered.connect(self._on_send_process)
        state_configurando.entered.connect(self._on_send_configure)
        state_envio.entered.connect(self._on_send_send)
        state_mimir.entered.connect(self._on_send_sleep)
        state_activo.entered.connect(self._on_active)

        self.ui_active.pushButton_esp_active_start_stop.clicked.connect(lambda: self.machine.postEvent(ESPActiveEvent()))
    
        state_proceso_envio.setInitialState(state_configurando)
        self.machine.setInitialState(state_encontrado)
        self.machine.start()

    def _on_active(self):
        self.start_btn.set_start_button()
        #self.send_status.set_send_status_default()
        self.ui_active.pushButton_remove.setDisabled(False)


    def _on_send_process(self):
        self.start_btn.set_restart_button()
        self.ui_active.pushButton_remove.setDisabled(True)
        self.ui_active.pushButton_esp_active_start_stop.setDisabled(True)
        #save all values into BD
        self.config.wifi_ui.save_ui_into_properties()
        self.config._save_config_into_model()

    def _on_send_configure(self):
        self.start_btn.ui_button.setDisabled(True)
        self.ui_active.pushButton_esp_active_start_stop.setDisabled(True)
        self.send_status.set_send_status_config()

        self.worker_slot()
        
        


    def _on_send_send(self):
        self.start_btn.ui_button.setDisabled(False)
        self.ui_active.pushButton_esp_active_start_stop.setDisabled(False)
        self.send_status.set_send_status_send()

    def _on_send_sleep(self):
        self.start_btn.ui_button.setDisabled(False)
        self.ui_active.pushButton_esp_active_start_stop.setDisabled(False)
        self.send_status.set_send_status_deepsleep()

    def _on_finish(self):
        self.config.machine.postEvent(InactiveESPEvent())
        self.esp_lists_machine.machine.postEvent(ESPRemoveActiveEvent(self.active_widget))
        self.esp_dict.remove_esp(self.esp_id)
        print("Finished!")

    def _found_to_active_slot(self):
        self.machine.postEvent(ESPActiveEvent())
        self.active_widget.setVisible(True)
        self.esp_lists_machine.machine.postEvent(ESPAddActiveEvent(self.active_widget))
        self.esp_lists_machine.machine.postEvent(ESPRemoveFoundEvent(self.found_widget))

    def notify_config_success(self):
        self.send_status.set_send_status_config(". Succeded!")
        self.machine.postEvent(ESPSendingEvent())

    def  notify_ble_try_failed(self, qty):
        self.send_status.set_send_status_error(configuring=True, extra_msg=". Tried {} times.".format(qty))

    def perform_ble_config(self):
        self.worker_ble = ConfigESPBLEWorker(self.main_win, self, self.gui_controller.configSetup)
        thread = QThread()
        self.worker_ble.setup_thread(thread)
        self.thread = thread
        thread.start()

    def perform_wifi_config(self):
        self.worker_wifi = ConfigESPWifiWorker(self.main_win, self, self.controller.rasp_.start_status20)
        thread = QThread()
        self.worker_wifi.setup_thread(thread)
        self.thread = thread
        thread.start()

    def set_found_widget(self) -> QFrame:
        ui_found = esp_found_item.Ui_Form_esp_found_item()
        found_frame = QFrame()
        ui_found.setupUi(found_frame)
        self.add_btn = ui_found.pushButton_esp_found_add
        self.found_widget = found_frame

        self.add_btn.clicked.connect(self._found_to_active_slot)
        self.ui_found = ui_found
        self.esp_lists_machine.machine.postEvent(ESPAddFoundEvent(self.found_widget))
        return found_frame

    def open_config_dialog(self):
        """
        config_dialog = QDialog(self.main_win)
        if self.ui_config_win == None:
            ui_config = esp_config_win.Ui_Dialog_esp_config()
            self.ui_config_win = ui_config
        self.ui_config_win.setupUi(config_dialog)
        """
        if self.ui_config_dialog.isVisible:
            self.config.status_ui.load_from_properties_into_ui()
            self.ui_config_dialog.show()

    def set_active_widget(self):
        ui_wifi = esp_wifi_config.Ui_Form_wifi_config()
        wifi_frame = QFrame()
        ui_wifi.setupUi(wifi_frame)
        self.ui_wifi = ui_wifi

        ui_active = esp_active_item.Ui_Form_esp_active()
        active_frame = QFrame()
        ui_active.setupUi(active_frame)
        self.ui_active = ui_active
        
        ui_active.pushButton_config_medium_bluetooth
        ui_active.pushButton_config_medium_bd

        ui_active.verticalLayout_wifi_config_expandable.addWidget(wifi_frame)

        ui_active.toolButton_esp_active_wifi_config.setContent(wifi_frame)

        ui_active.pushButton_esp_active_config.clicked.connect(self.open_config_dialog)
        self.active_widget = active_frame

        ui_active.pushButton_remove.clicked.connect(lambda: self.machine.postEvent(InactiveESPEvent()))

        self.config = ESPConfig(self)
        self.config.set_machine()