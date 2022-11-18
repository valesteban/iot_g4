from queue import Queue
from multiprocessing import Process, Lock

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDialog, QPushButton, QLabel, QWidget, QLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QStateMachine, QState, QTimer, QObject, QEvent, QAbstractTransition, QEventTransition
import typing

from forms import main_display, esp_found_item, esp_active_item,  esp_wifi_config, esp_config_win, live_plot

#region Events

class EndFindEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+1
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPFoundEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+2
    def __init__(self, esp_id, esp_mac) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_id = esp_id
        self.esp_mac = esp_mac

class ESPAddFoundEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+3
    def __init__(self,esp_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_widget = esp_widget

# used only to signal a transition within the ESP object itself
class ESPActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+4
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPAddActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+5
    def __init__(self, esp_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_widget = esp_widget

class ESPRemoveActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+6
    def __init__(self, esp_id, esp_mac) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_id = esp_id
        self.esp_mac = esp_mac

class CheckNoWifiEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+7
    def __init__(self, config_wifi: bool, send_wifi: bool) -> None:
        super().__init__(self.EVENT_TYPE)
        self.config_wifi = config_wifi
        self.send_wifi = send_wifi

class UnableToSendEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+8
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class AbleToSendEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+9
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class InvalidWifiConfigEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+10
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ValidWifiConfigEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+11
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

#endregion


#region Transitions

class EndFindTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != EndFindEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPFoundTransition(QAbstractTransition):
    def __init__(self, esp_list: "ESPDicts", sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.found_event = None
        self.esp_list = esp_list

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPFoundEvent.EVENT_TYPE:
        
            return False
        else:
            self.found_event = event
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 

    def transition_slot(self):
        print("hellow")
        print(self.found_event.esp_id, self.found_event.esp_mac)
        self.esp_list.check_esp(self.found_event.esp_id, self.found_event.esp_mac)

class ESPAddFoundTransition(QAbstractTransition):
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddFoundEvent.EVENT_TYPE:
            return False
        else:
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 

class ESPActiveTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = ...) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPActiveEvent.EVENT_TYPE:
            return False
        else:
            return True
            

class ESPAddActiveTransition(QAbstractTransition):
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddActiveEvent.EVENT_TYPE:
            return False
        else:
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 

class CheckNoWifiTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != CheckNoWifiEvent.EVENT_TYPE:
            return False
        else:
            if not event.config_wifi and not event.send_wifi:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return 

class UnableToSendTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != UnableToSendEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class AbleToSendTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != AbleToSendEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class InvalidWifiConfigTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != InvalidWifiConfigEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class ValidWifiConfigTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ValidWifiConfigEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return


#endregion

#region Machines

class ESPStateMachine(QStateMachine):
    def __init__(self, esp_id, esp_mac, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.esp_id = esp_id
        self.esp_mac = esp_mac

    def onEntry(self, event: QEvent) -> None:
        return super().onEntry(event)

#endregion

#region States

class FoundState(QState):
    def __init__(self, esp: "ESP", parent: typing.Optional['QState'] = None) -> None:
        super().__init__(parent)
        self.esp = esp

    def onEntry(self, event: QEvent) -> None:
        self.esp.set_found_widget()
        return super().onEntry(event)

    

#endregion


class ListsMachine:
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, widget_active_list_parent: QWidget, list_active_layout: QLayout) -> None:
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout
        self.widget_active_list_parent = widget_active_list_parent
        self.active_list_layout = list_active_layout

        self.machine = QStateMachine()
        state_fempty_ampty = QState(self.machine)
        state_found_ampty = QState(self.machine)
        state_fempty_active = QState(self.machine)
        state_found_active = QState(self.machine)

        # add ESP item to found list
        trans_fe_ae_f_ae = ESPAddFoundTransition(self.widget_list_parent, self.list_layout)
        trans_fe_ae_f_ae.setTargetState(state_found_ampty)
        state_fempty_ampty.addTransition(trans_fe_ae_f_ae)

        trans_f_ae = ESPAddFoundTransition(self.widget_list_parent, self.list_layout)
        state_found_ampty.addTransition(trans_f_ae)

        trans_fe_a_f_a = ESPAddFoundTransition(self.widget_list_parent, self.list_layout)
        trans_fe_a_f_a.setTargetState(state_found_active)
        state_fempty_active.addTransition(trans_fe_a_f_a)

        trans_f_a = ESPAddFoundTransition(self.widget_list_parent, self.list_layout)
        state_found_active.addTransition(trans_f_a)

        # add ESP item to active list
        trans_f_ae_fa_a = ESPAddActiveTransition(self.widget_active_list_parent,self.active_list_layout)
        trans_f_ae_fa_a.setTargetState(state_fempty_active)
        state_found_ampty.addTransition(trans_f_ae_fa_a)

        self.machine.setInitialState(state_fempty_ampty)
        self.machine.start()

class ESPDicts:
    def __init__(self, esp_lists_machine, main_win) -> None:
        self.mutex = Lock()
        self.esp_lists_machine = esp_lists_machine
        self.main_win = main_win

        self.esp_dict = dict()

    def check_esp(self, esp_id, esp_mac):
        try:
            self.mutex.acquire()
            if esp_id not in self.esp_dict.keys():
                self.esp_dict[esp_id] = ESP(esp_id, esp_mac, self.esp_lists_machine, self, self.main_win)
                self.esp_dict[esp_id].set_machine()
            else:
                self.esp_dict[esp_id].machine.postEvent(ESPFoundEvent(esp_id, esp_mac))
        finally:
            self.mutex.release()

    def remove_esp() -> None:
        pass

class ESPConfig:
    def __init__(self, esp: "ESP") -> None:
        self.esp = esp
        self.machine: QStateMachine = None

        self.config_wifi = None
        self.send_wifi = False

    def set_medium_and_post(self, config_wifi: bool=None, send_wifi:bool=None):
        if config_wifi is not None:
            self.config_wifi = config_wifi
        if send_wifi is not None:
            self.send_wifi = send_wifi
        self.machine.postEvent(CheckNoWifiEvent(self.config_wifi, self.send_wifi))

    def set_machine(self) ->None:
        self.machine = QStateMachine()
        state_config_paralell = QState(childMode=QState.ChildMode.ParallelStates, parent=self.machine) 

        state_configs = QState(state_config_paralell)
        state_can_send = QState(state_config_paralell)

        state_no_config = QState(state_configs)
        state_config_wifi = QState(state_configs)
        state_config_no_wifi = QState(state_configs)
        state_wifi_error = QState(state_configs)

        state_unable_to_send = QState(state_can_send)
        state_able_to_send = QState(state_can_send)

        state_configs.setInitialState(state_no_config)
        state_can_send.setInitialState(state_unable_to_send)

        self.machine.setInitialState(state_config_paralell)

        self.esp.ui_active.pushButton_config_medium_bluetooth.clicked.connect(lambda: self.set_medium_and_post(config_wifi=False))
        self.esp.ui_active.pushButton_config_medium_bd.clicked.connect(lambda: self.set_medium_and_post(config_wifi=True))
        self.esp.ui_config_win.pushButton_send_bluetooth.clicked.connect(lambda: self.set_medium_and_post(send_wifi=False))
        self.esp.ui_config_win.pushButton_send_wifi.clicked.connect(lambda: self.set_medium_and_post(send_wifi=True))

        # la idea es abrir la ventana de configuración cuando la rasp no ha sido previamente configurada
        state_no_config.exited.connect(self.esp.open_config_dialog)
        state_no_config.addTransition(self.esp.ui_active.pushButton_config_medium_bluetooth.clicked, state_config_no_wifi)
        state_no_config.addTransition(self.esp.ui_active.pushButton_config_medium_bd.clicked, state_config_wifi)

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

        def _check_valid_connections():
            if self.config_wifi is None or self.send_wifi is None:
                self.machine.postEvent(UnableToSendEvent())
            else:
                self.machine.postEvent(AbleToSendEvent())

        state_config_wifi.entered.connect(_auto_show_toolbar)
        state_config_no_wifi.entered.connect(_auto_hide_toolbar)

        state_config_wifi.entered.connect(_check_valid_connections)
        state_config_no_wifi.entered.connect(_check_valid_connections)

        self.machine.start()
    

class ESP:
    def __init__(self, esp_id, esp_mac, esp_lists_machine: ListsMachine, esp_dict_list: "ESPDicts", main_win) -> None:
        self.esp_id = esp_id
        self.esp_mac = esp_mac
        self.machine: QStateMachine = None
        self.esp_lists_machine: ListsMachine = esp_lists_machine
        self.esp_dict = esp_dict_list
        self.main_win = main_win

        self.found_widget = None
        self.add_btn: QPushButton = None
        self.ui_active: esp_active_item.Ui_Form_esp_active = None
        self.ui_wifi: esp_wifi_config.Ui_Form_wifi_config = None

        self.ui_config_dialog = QDialog(self.main_win)
        self.ui_config_win: esp_config_win.Ui_Dialog_esp_config = esp_config_win.Ui_Dialog_esp_config()
        self.ui_config_win.setupUi(self.ui_config_dialog)

        self.config: ESPConfig = None


    def set_machine(self) -> None:
        self.machine = QStateMachine()
        state_encontrado = FoundState(self, self.machine)
        state_activo = QState(self.machine)
        state_dead = QState(self.machine)
        state_envio = QState(self.machine)
 

        #state_encontrado.addTransition(_found_to_active_slot, state_activo)

        trans_make_active = ESPFoundTransition(self.esp_dict)
        trans_make_active.setTargetState(state_activo)
        state_dead.addTransition(trans_make_active)

        self.machine.setInitialState(state_encontrado)
        self.machine.start()

    def _found_to_active_slot(self):
        self.machine.postEvent(ESPActiveEvent())
        self.set_active_widget()
        self.esp_lists_machine.machine.postEvent(ESPAddActiveEvent(self.active_widget))

    def set_found_widget(self):
        ui_found = esp_found_item.Ui_Form_esp_found_item()
        found_frame = QFrame()
        ui_found.setupUi(found_frame)
        self.add_btn = ui_found.pushButton_esp_found_add
        self.found_widget = found_frame

        self.add_btn.clicked.connect(self._found_to_active_slot)

        self.esp_lists_machine.machine.postEvent(ESPAddFoundEvent(self.found_widget))

    def open_config_dialog(self):
        """
        config_dialog = QDialog(self.main_win)
        if self.ui_config_win == None:
            ui_config = esp_config_win.Ui_Dialog_esp_config()
            self.ui_config_win = ui_config
        self.ui_config_win.setupUi(config_dialog)
        """
        if self.ui_config_dialog.isVisible:
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

        self.config = ESPConfig(self)
        self.config.set_machine()




    

class QStateTimer(QState):
    def __init__(self, t_timeout= 1000):
        super().__init__()
        self.timer = QTimer(self)
        self.t_timeout = t_timeout

    def _timer_slot(self):
        print("timeout!!")

    def onEntry(self, event: QEvent) -> None:
        print("entered buscando")
        self.timer.singleShot(self.t_timeout, self._timer_slot)
        return super().onEntry(event)
        
    def addTransitionTimeout(self, state):
        return super().addTransition(self.timer.timeout, state)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    ui_main_disp = main_display.Ui_MainWindow()
    ui_main_disp.setupUi(window)

    debug_dialog = QDialog(window)
    verticalLayout_debug= QtWidgets.QVBoxLayout(debug_dialog)

    esp_found_label = QLabel("Found window", debug_dialog)
    btn_end_find = QPushButton("End find", debug_dialog)
    esp_1_label = QtWidgets.QLabel("ESP1", debug_dialog)
    esp_1_btn_found = QtWidgets.QPushButton("found", debug_dialog)

    verticalLayout_debug.addWidget(esp_found_label)
    verticalLayout_debug.addWidget(btn_end_find)
    verticalLayout_debug.addWidget(esp_1_label)
    verticalLayout_debug.addWidget(esp_1_btn_found)


    ## machinery

    machine_buscando = QStateMachine()
    state_buscando = QState()
    state_sin_buscar = QState()

    state_sin_buscar.addTransition(ui_main_disp.pushButton_search_refresh.clicked, state_buscando)
    
    endfind_transition = EndFindTransition()
    endfind_transition.setTargetState(state_sin_buscar)
    state_buscando.addTransition(endfind_transition)

    state_buscando.assignProperty(ui_main_disp.pushButton_search_refresh, "enabled", False)
    state_sin_buscar.assignProperty(ui_main_disp.pushButton_search_refresh, "enabled", True)

    machine_buscando.addState(state_buscando)
    machine_buscando.addState(state_sin_buscar)
    machine_buscando.setInitialState(state_sin_buscar)

    esp_list = ListsMachine(
        ui_main_disp.scrollAreaWidgetContents_found_area, 
        ui_main_disp.verticalLayout_found_list,
        ui_main_disp.scrollAreaWidgetContents_active_esp,
        ui_main_disp.verticalLayout_active_list)
    esp_dict_list = ESPDicts(esp_list, window)

    found_trans = ESPFoundTransition(esp_dict_list)
    state_buscando.addTransition(found_trans)
    found_trans.triggered.connect(found_trans.transition_slot)

    

    

    ## Buttons signals
    btn_end_find.clicked.connect(lambda: machine_buscando.postEvent(EndFindEvent()))
    esp_1_btn_found.clicked.connect(lambda: machine_buscando.postEvent(ESPFoundEvent(1110, "aa-bb-cc-dd-ee-ff")))



    def add_found_item():
        ui_found = esp_found_item.Ui_Form_esp_found_item()
        found_frame = QFrame()
        ui_found.setupUi(found_frame)
        
        ui_main_disp.verticalLayout_found_list.addWidget(found_frame)

    #ui_main_disp.pushButton_search_refresh.clicked.connect(add_found_item)

    def add_active_item():
        ui_wifi = esp_wifi_config.Ui_Form_wifi_config()
        wifi_frame = QFrame()
        ui_wifi.setupUi(wifi_frame)

        ui_active = esp_active_item.Ui_Form_esp_active()
        active_frame = QFrame()
        ui_active.setupUi(active_frame)

        ui_active.verticalLayout_wifi_config_expandable.addWidget(wifi_frame)

        ui_active.toolButton_esp_active_wifi_config.setContent(wifi_frame)

        def open_config_dialog():
            ui_config = esp_config_win.Ui_Dialog_esp_config()
            config_dialog = QDialog(window)
            ui_config.setupUi(config_dialog)
            config_dialog.show()

        ui_main_disp.verticalLayout_active_list.addWidget(active_frame)

        ui_active.pushButton_esp_active_config.clicked.connect(open_config_dialog)



    #ui_main_disp.pushButton_search_refresh.clicked.connect(add_active_item)

    def add_live_plot():
        ui_plot = live_plot.Ui_Form_live_plot()
        plot_frame = QFrame()
        ui_plot.setupUi(plot_frame)
        ui_main_disp.verticalLayout_added_plots_list.addWidget(plot_frame)

    ui_main_disp.pushButton_add_live_plot.clicked.connect(add_live_plot)

    window.show()
    debug_dialog.show()
    machine_buscando.start()

    sys.exit(app.exec())