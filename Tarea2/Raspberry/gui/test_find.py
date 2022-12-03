import re
from queue import Queue
from multiprocessing import Process, Lock

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDialog, QPushButton, QLabel, QWidget, QLayout, QSpinBox, QLineEdit, QComboBox, QStackedWidget, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QStateMachine, QState, QFinalState, QTimer, QObject, QEvent, QAbstractTransition, QEventTransition, pyqtProperty, pyqtSignal, QMetaType, QSignalTransition
import typing

from forms import main_display, esp_found_item, esp_active_item,  esp_wifi_config, esp_config_win, live_plot

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.legend import _get_legend_handles_labels
import numpy as np

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

class ESPRemoveFoundEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+4
    def __init__(self,esp_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_widget = esp_widget

# used only to signal a transition within the ESP object itself
class ESPActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+5
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPAddActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+6
    def __init__(self, esp_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_widget = esp_widget

class ESPRemoveActiveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+7
    def __init__(self, esp_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.esp_widget = esp_widget

class CheckNoWifiEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+8
    def __init__(self, config_wifi: bool, send_wifi: bool) -> None:
        super().__init__(self.EVENT_TYPE)
        self.config_wifi = config_wifi
        self.send_wifi = send_wifi

class UnableToSendEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+9
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class AbleToSendEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+10
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class InvalidWifiConfigEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+11
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ValidWifiConfigEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+12
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class SendStartEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+13
    def __init__(self) ->None:
        super().__init__(self.EVENT_TYPE)

# internal ESP state when it is either removed from active list and found list
class InactiveESPEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+14    
    def __init__(self) ->None:
        super().__init__(self.EVENT_TYPE)

class LivePlotAddEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+15
    def __init__(self,plot_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.plot_widget = plot_widget

class LivePlotRemoveEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+16
    def __init__(self,plot_widget) -> None:
        super().__init__(self.EVENT_TYPE)
        self.plot_widget = plot_widget


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
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddFoundEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_found += 1
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPRemoveFoundTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPRemoveFoundEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_found -= 1
            
            self.list_layout.removeWidget(event.esp_widget)
            event.esp_widget.setParent(None)
            if self.esp_lists.num_found == 0:
                return True
            return False

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
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddActiveEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_active += 1
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPRemoveActiveTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPRemoveActiveEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_active -= 1
            self.list_layout.removeWidget(event.esp_widget)
            event.esp_widget.setParent(None)
            
            if self.esp_lists.num_active == 0:
                return True
            return False

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

class SendStartTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != SendStartEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class InactiveESPTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != InactiveESPEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class LivePlotAddTransition(QAbstractTransition):
    def __init__(self, plot_lists: "PlotListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.plot_lists = plot_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotAddEvent.EVENT_TYPE:
            return False
        else:
            self.plot_lists.num_plots += 1
            event.plot_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.plot_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class LivePlotRemoveTransition(QAbstractTransition):
    def __init__(self, plot_lists: "PlotListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.plot_lists = plot_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotRemoveEvent.EVENT_TYPE:
            return False
        else:
            self.plot_lists.num_plots -= 1
            
            self.list_layout.removeWidget(event.plot_widget)
            event.plot_widget.setParent(None)
            if self.plot_lists.num_plots == 0:
                return True
            return False

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
        self.esp.found_widget.setVisible(True)
        return super().onEntry(event)

    

#endregion

#region Properties
class WifiProperties(QObject):
    host_changed = pyqtSignal(str)
    tcp_changed = pyqtSignal(int)
    udp_changed = pyqtSignal(int)
    ssid_changed = pyqtSignal(str)
    passwd_changed = pyqtSignal(str)

    host_invalidated = pyqtSignal()
    tcp_invalidated = pyqtSignal()
    udp_invalidated = pyqtSignal()
    ssid_invalidated = pyqtSignal()
    passwd_invalidated = pyqtSignal()

    host_re = r"^"+"[.]".join([r"(?P<byte_"+str(i)+">25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})" for i in range(1,5)]) + r"$"
    attrs = ["host_ipv4", "port_tcp", "port_udp", "ssid", "passwd"]

    def __init__(self):
        QObject.__init__(self)
        self._host_ipv4 = "255.255.255.255"
        self._port_tcp = 5000
        self._port_udp = 5000
        self._ssid: QMetaType.Type.QString = ""
        self._passwd: QMetaType.Type.QString = ""

    #Host IP
    def read_host_ipv4(self):
        return self._host_ipv4

    def set_host_ipv4(self, new_ip):
        if new_ip != self._host_ipv4:
            if self.validate_host_ipv4(new_ip):
                self._host_ipv4 = new_ip
                self.host_changed.emit(new_ip)

    def validate_host_ipv4(self, new_ip):
        m = re.match(self.host_re, new_ip)
        if m is not None:
            return True
        else:
            self.host_invalidated.emit()
            return False

    def reset_host_ipv4(self):
        self._host_ipv4 = "255.255.255.255"

    

    #TCP
    def read_port_tcp(self):
        return self._port_tcp

    def set_port_tcp(self, new_port):
        if new_port != self._port_tcp:
            if self.validate_port_tcp(new_port):
                self._port_tcp = new_port
                self.tcp_changed.emit(new_port)

    def validate_port_tcp(self, new_port):
        if new_port < 2**16:
            return True
        else:
            self.tcp_invalidated.emit()
            return False

    def reset_port_tcp(self):
        self._port_tcp = 5000

    

    #UDP
    def read_port_udp(self):
        return self._port_udp

    def set_port_udp(self, new_port):
        if new_port != self._port_udp:
            if self.validate_port_udp(new_port):
                self._port_udp = new_port
                self.udp_changed.emit(new_port)

    def validate_port_udp(self, new_port):
        if new_port < 2**16:
            return True
        else:
            self.udp_invalidated.emit()
            return False

    def reset_port_udp(self):
        self._port_udp = 5000

    

    #SSID
    def read_ssid(self):
        return self._ssid

    def set_ssid(self, new_ssid):
        if new_ssid != self._ssid:
            if self.validate_ssid(new_ssid):
                self._ssid = new_ssid
                self.ssid_changed.emit(new_ssid)

    def validate_ssid(self, new_ssid):
        if new_ssid != "":
            return True
        else:
            self.ssid_invalidated.emit()
            return False

    def reset_ssid(self):
        self._ssid = "dummy"

    #Passwd
    def read_passwd(self):
        return self._passwd

    def set_passwd(self, new_passwd):
        if new_passwd != self._passwd:
            if self.validate_passwd(new_passwd):
                self._passwd = new_passwd
                self.passwd_changed.emit(new_passwd)

    def validate_passwd(self, new_passwd):
        if new_passwd != "":
            return True
        else:
            self.passwd_invalidated.emit()
            return False

    def reset_passwd(self):
        self._passwd = "dummy"

    # utility functions
    def validate_all(self, *vals):
        result = True
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            mid_result = getattr(self, "validate_"+attr)(vals[i])
            result = result and mid_result
        return result

    def set_all(self, *new_vals):
        assert len(new_vals) == len(self.attrs)
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, "set_"+ attr)(new_vals[i])
        
    def get_all(self):
        return [getattr(self, attr) for attr in self.attrs]

    host_ipv4 = pyqtProperty(str, read_host_ipv4, set_host_ipv4, notify=host_changed)
    port_tcp = pyqtProperty(int, read_port_tcp, set_port_tcp, notify=tcp_changed)
    port_udp = pyqtProperty(int, read_port_udp, set_port_udp, notify=udp_changed)
    ssid = pyqtProperty(str, read_ssid, set_ssid, notify=ssid_changed)
    passwd = pyqtProperty(str, read_passwd, set_passwd, notify=passwd_changed)


class ConfigProperties(QObject):
    status_conf_changed = pyqtSignal(int)
    protocol_conf_changed = pyqtSignal(int)
    discontinuous_time_changed = pyqtSignal(int)
    acc_sampling_changed = pyqtSignal(int)
    acc_sensibility_changed = pyqtSignal(int)
    gyro_sensibility_changed = pyqtSignal(int)
    bme668_sampling_changed = pyqtSignal(int)

    status_conf_invalidated = pyqtSignal()
    protocol_conf_invalidated = pyqtSignal()
    discontinuous_time_invalidated = pyqtSignal()
    acc_sampling_invalidated = pyqtSignal()
    acc_sensibility_invalidated = pyqtSignal()
    gyro_sensibility_invalidated = pyqtSignal()
    bme668_sampling_invalidated = pyqtSignal()

    statuses_conf = { 21, 22, 23, 30, 31 }
    protocols_conf = { i for i in range(1,6) }
    acc_samplings = { 10, 100, 400, 1000 } 
    acc_sensibilities = { 2,4,8,16 }
    gyro_sensibilities = { 200, 250, 500 }
    bme_samplings = { 1,2,3,4 }

    attrs = ["status_conf", "protocol_conf", "discontinuous_time", "acc_sampling", "acc_sensibility", "gyro_sensibility", "bme668_sampling"]

    def __init__(self):
        QObject.__init__(self)
        self._status_conf = 21
        self._protocol_conf = 1
        self._discontinuous_time = 60
        self._acc_sampling = 10
        self._acc_sensibility = 2
        self._gyro_sensibility = 200
        self._bme668_sampling = 1

    # status_conf
    def read_status_conf(self):
        return self._status_conf

    def set_status_conf(self, new_status):
        if self._status_conf != new_status:
            if self.validate_status_conf(new_status):
                self._status_conf = new_status
                self.status_conf_changed.emit(new_status)

    def validate_status_conf(self, new_status):
        if new_status in self.statuses_conf:
            return True
        else:
            self.status_conf_invalidated.emit()
            return False

    def reset_status_conf(self):
        self._status_conf = 21

    # protocol_conf
    def read_protocol_conf(self):
        return self._protocol_conf

    def set_protocol_conf(self, new_protocol):
        if self._protocol_conf != new_protocol:
            if self.validate_protocol_conf(new_protocol):
                self._protocol_conf = new_protocol
                self.protocol_conf_changed.emit(new_protocol)

    def validate_protocol_conf(self, new_protocol):
        if new_protocol in self.protocols_conf:
            return True
        else:
            self.protocol_conf_invalidated.emit()
            return False

    def reset_protocol_conf(self):
        self._protocol_conf = 1

    # discontinuous time
    def read_discontinuous_time(self):
        return self._discontinuous_time

    def set_discontinuous_time(self, new_time):
        if self._discontinuous_time != new_time:
            if self.validate_discontinuous_time(new_time):
                self._discontinuous_time = new_time
                self.discontinuous_time_changed.emit(new_time)

    def validate_discontinuous_time(self, new_time):
        if new_time >= 10:
            return True
        else:
            self.discontinuous_time_invalidated.emit()
            return False

    def reset_discontinuous_time(self):
        self._discontinuous_time = 60

    #acc_sampling
    def read_acc_sampling(self):
        return self._acc_sampling

    def set_acc_sampling(self, new_sample):
        if self._acc_sampling != new_sample:
            if self.validate_acc_sampling(new_sample):
                self._acc_sampling = new_sample
                self.acc_sampling_changed.emit(new_sample)

    def validate_acc_sampling(self, new_sample):
        if new_sample in self.acc_samplings:
            return True
        else:
            self.acc_sampling_invalidated.emit()
            return False

    def reset_acc_sampling(self):
        self._acc_sampling = 10


    #acc_sensibility
    def read_acc_sensibility(self):
        return self._acc_sensibility

    def set_acc_sensibility(self, new_sensibility):
        if self._acc_sensibility != new_sensibility:
            if self.validate_acc_sensibility(new_sensibility):
                self._acc_sensibility = new_sensibility
                self.acc_sensibility_changed.emit(new_sensibility)

    def validate_acc_sensibility(self, new_sensibility):
        if new_sensibility in self.acc_sensibilities:
            return True
        else:
            self.acc_sensibility_invalidated.emit()
            return False

    def reset_acc_sensibility(self):
        self._acc_sensibility = 2


    #gyro_sensibility
    def read_gyro_sensibility(self):
        return self._gyro_sensibility

    def set_gyro_sensibility(self, new_sensibility):
        if self._gyro_sensibility != new_sensibility:
            if self.validate_gyro_sensibility(new_sensibility):
                self._gyro_sensibility = new_sensibility
                self.gyro_sensibility_changed.emit(new_sensibility)

    def validate_gyro_sensibility(self, new_sensibility):
        if new_sensibility in self.gyro_sensibilities:
            return True
        else:
            self.gyro_sensibility_invalidated.emit()
            return False

    def reset_gyro_sensibility(self):
        self._gyro_sensibility = 200


    #gyro_sensibility
    def read_bme668_sampling(self):
        return self._bme668_sampling

    def set_bme668_sampling(self, new_sample):
        if self._bme668_sampling != new_sample:
            if self.validate_bme668_sampling(new_sample):
                self._bme668_sampling = new_sample
                self.bme668_sampling_changed.emit(new_sample)

    def validate_bme668_sampling(self, new_sample):
        if new_sample in self.bme_samplings:
            return True
        else:
            self.bme668_sampling_invalidated.emit()
            return False

    def reset_bme668_sampling(self):
        self._bme668_sampling = 1

    # utility functions
    def validate_all(self, *vals):
        result = True
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            mid_result = getattr(self, "validate_"+attr)(vals[i])
            result = result and mid_result
        return result

    def set_all(self, *new_vals):
        assert len(new_vals) == len(self.attrs)
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, "set_"+ attr)(new_vals[i])
        
    def get_all(self):
        return [getattr(self, attr) for attr in self.attrs]

    status_conf = pyqtProperty(int, read_status_conf, set_status_conf, freset=reset_status_conf, notify=status_conf_changed)
    protocol_conf = pyqtProperty(int, read_protocol_conf, set_protocol_conf, freset=reset_protocol_conf, notify=protocol_conf_changed)
    discontinuous_time = pyqtProperty(int, read_discontinuous_time, set_discontinuous_time, freset=reset_discontinuous_time, notify=discontinuous_time_changed)
    acc_sampling = pyqtProperty(int, read_acc_sampling, set_acc_sampling, freset=reset_acc_sampling, notify=acc_sampling_changed)
    acc_sensibility = pyqtProperty(int, read_acc_sensibility, set_acc_sensibility, freset=reset_acc_sensibility, notify=acc_sensibility_changed)
    gyro_sensibility = pyqtProperty(int, read_gyro_sensibility, set_gyro_sensibility, freset=reset_gyro_sensibility, notify=gyro_sensibility_changed)
    bme668_sampling = pyqtProperty(int, read_bme668_sampling, set_bme668_sampling, freset=reset_bme668_sampling, notify=bme668_sampling_changed)


class WifiIputUI(QObject):
    base_style = ""
    border_default_style = "border: 1px solid rgb(122, 122, 122);"
    border_invalid_style = "border: 1px solid red"
    
    label_parent = "Form_wifi_config"
    default_err_msg = "Invalid field input"
    _translate = QtCore.QCoreApplication.translate

    default_msg_color = QtGui.QColor(120, 120, 120)
    err_msg_color = QtGui.QColor(255, 0, 0)
    warn_msg_color = QtGui.QColor(244, 146, 0)

    def __init__(self, input_ui: QWidget, msg_label: QLabel) -> None:
        QObject.__init__(self)
        self.ui_input = input_ui
        self.ui_msg = msg_label

    def set_default_box_view(self):
        self.ui_input.setStyleSheet(self.base_style + self.border_default_style)

    def set_invalid_box_view(self):
        self.ui_input.setStyleSheet(self.base_style + self.border_invalid_style)

    def set_msg_text(self, msg: str=""):
        if msg == "":
            msg = self.default_err_msg
        self.ui_msg.setText(self._translate(self.label_parent, msg))

    def set_msg_visibility(self, val: bool):
        self.ui_msg.setVisible(val)

    def set_msg_status_error(self):
        self.set_msg_txt_color(self.err_msg_color, self.err_msg_color)

    def set_msg_status_warning(self):
        self.set_msg_txt_color(self.warn_msg_color, self.warn_msg_color)

    def set_msg_txt_color(self,color_active=None, color_inactive=None, color_disabled=None):
        if color_active is None:
            color_active = self.default_msg_color
        if color_inactive is None:
            color_inactive = self.default_msg_color
        if color_disabled is None:
            color_disabled = self.default_msg_color
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(color_active)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        
        brush = QtGui.QBrush(color_inactive)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        
        brush = QtGui.QBrush(color_disabled)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

        self.ui_msg.setPalette(palette)

    def set_normal_status(self):
        self.set_default_box_view()
        self.set_msg_visibility(False)

    def set_error_status(self, msg=""):
        self.set_invalid_box_view()
        self.set_msg_status_error()
        self.set_msg_text(msg)
        self.set_msg_visibility(True)

    def set_warn_status(self, msg=""):
        self.set_default_box_view()
        self.set_msg_status_warning()
        self.set_msg_text(msg)
        self.set_msg_visibility(True)

    def getVal(self):
        pass

    def setVal(self):
        pass

    def get_signal(self):
        pass


class HostIPBar(WifiIputUI):
    base_style = "background:white;\n"
    ip_changed = pyqtSignal(str)
    
    def __init__(self, ui_host_bar: QtWidgets.QGroupBox, spinbox_array: list[QSpinBox], msg_label) -> None:
        super().__init__(ui_host_bar, msg_label)
        self.spinbox_array = spinbox_array
        self.set_changed_emission()

    def getVal(self) -> str:
        result = ".".join([str(spin.value()) for spin in self.spinbox_array])
        return result

    def setVal_from_list(self, *byte_values: list[int]):
        assert len(byte_values) == len(self.spinbox_array)
        for i in range(len(self.spinbox_array)):
            spin = self.spinbox_array[i]
            spin.setProperty("value", byte_values[i])

    def setVal(self, host_ip: str):
        self.setVal_from_list(*host_ip.split("."))
    
    def set_changed_emission(self):
        def emit_slot():
            self.ip_changed.emit(self.getVal())

        for spin in self.spinbox_array:
            spin.valueChanged.connect(emit_slot)
    
    def get_signal(self):
        return self.ip_changed


class WifiSpinboxUI(WifiIputUI):
    def __init__(self, input_ui: QSpinBox, msg_label: QLabel) -> None:
        super().__init__(input_ui, msg_label)

    def getVal(self):
        return self.ui_input.value()

    def setVal(self, newVal: int):
        self.ui_input.setProperty("value", newVal)

    def get_signal(self):
        return self.ui_input.valueChanged


class WifiLineEditUI(WifiIputUI):
    def __init__(self, input_ui: QLineEdit, msg_label: QLabel) -> None:
        super().__init__(input_ui, msg_label)

    def getVal(self):
        return self.ui_input.text()

    def setVal(self, new_text: str):
        self.ui_input.setText(new_text)

    def get_signal(self):
        return self.ui_input.textEdited


class WifiDisplay:
    attrs = ["host_ui", "tcp_ui", "udp_ui", "ssid_ui", "passwd_ui"]

    def __init__(self, ui_wifi: esp_wifi_config.Ui_Form_wifi_config, wifi_properties: WifiProperties):
        self.ui_wifi = ui_wifi
        self.wifi_properties = wifi_properties

        self.host_ui = HostIPBar(
            self.ui_wifi.groupBox_host_ip, 
            [self.ui_wifi.spinBox_byte_1,
            self.ui_wifi.spinBox_byte_2,
            self.ui_wifi.spinBox_byte_3,
            self.ui_wifi.spinBox_byte_4],
            self.ui_wifi.label_host_ip_status_msg)
        self.tcp_ui = WifiSpinboxUI(
            self.ui_wifi.spinBox_tcp_port,
            self.ui_wifi.label_tcp_port_status_msg)
        self.udp_ui = WifiSpinboxUI(
            self.ui_wifi.spinBox_udp_port,
            self.ui_wifi.label_udp_port_status_msg)
        self.ssid_ui = WifiLineEditUI(
            self.ui_wifi.lineEdit_ssid,
            self.ui_wifi.label_ssid_status_msg)
        self.passwd_ui = WifiLineEditUI(
            self.ui_wifi.lineEdit_pass,
            self.ui_wifi.label_pass_status_msg)

    def set_ui_to_default_view(self):
        [getattr(self, attr).set_normal_status() for attr in self.attrs]

    def get_signals(self):
        return [getattr(self, attr).get_signal() for attr in self.attrs]
        
    def set_invalid_signal_slots(self):
        self.wifi_properties.host_invalidated.connect(self.host_ui.set_error_status)
        self.wifi_properties.tcp_invalidated.connect(self.tcp_ui.set_error_status)
        self.wifi_properties.udp_invalidated.connect(self.udp_ui.set_error_status)
        self.wifi_properties.ssid_invalidated.connect(lambda: self.ssid_ui.set_error_status("This field is required"))
        self.wifi_properties.passwd_invalidated.connect(lambda: self.passwd_ui.set_error_status("This field is required"))

    def set_valid_signal_slots(self):
        self.wifi_properties.host_changed.connect(self.host_ui.set_normal_status)
        self.wifi_properties.tcp_changed.connect(self.tcp_ui.set_normal_status)
        self.wifi_properties.udp_changed.connect(self.udp_ui.set_normal_status)
        self.wifi_properties.ssid_changed.connect(self.ssid_ui.set_normal_status)
        self.wifi_properties.passwd_changed.connect(self.passwd_ui.set_normal_status)

    def get_all_ui_values(self):
        return [getattr(self, attr).getVal() for attr in self.attrs]

    def set_all_ui_values(self, *vals):
        assert len(vals) == len(self.attrs)
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, attr).setVal(vals[i])
    
    def save_ui_into_properties(self):
        self.wifi_properties.set_all(*self.get_all_ui_values())

    def load_from_properties_into_ui(self):
        self.set_all_ui_values(*self.wifi_properties.get_all())


class AbstractPortType:
    def __init__(self, udp_widgets) -> None:
        self.udp_widgets = udp_widgets

    def change_udp_visibility(self, bool_):
        [widget.setVisible(bool_) for widget in self.udp_widgets]

    def on_dynamic_change(self):
        pass

class PortTypeTCP(AbstractPortType):
    def __init__(self, udp_widgets) -> None:
        super().__init__(udp_widgets)

    def on_dynamic_change(self):
        self.change_udp_visibility(False)

class PortTypeUDP(AbstractPortType):
    def __init__(self, udp_widgets) -> None:
        super().__init__(udp_widgets)

    def on_dynamic_change(self):
        self.change_udp_visibility(True)

class AbstractDiscontinuousType:
    def __init__(self, disc_widgets) -> None:
        self.disc_widgets = disc_widgets

    def change_disc_widgets_visibility(self, bool_):
        [widget.setVisible(bool_) for widget in self.disc_widgets]

    def on_dynamic_change(self):
        pass

class TypeDiscontinuous(AbstractDiscontinuousType):
    def __init__(self, disc_widgets) -> None:
        super().__init__(disc_widgets)

    def on_dynamic_change(self):
        self.change_disc_widgets_visibility(True)

class TypeContinuous(AbstractDiscontinuousType):
    def __init__(self, disc_widgets) -> None:
        super().__init__(disc_widgets)

    def on_dynamic_change(self):
        self.change_disc_widgets_visibility(False)

class StatusUI(QObject):
    status_selected = pyqtSignal(object)

    def __init__(self, disc_type: AbstractDiscontinuousType, protocol_type: "ProtocolBaseUI",status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox) -> None:
        QObject.__init__(self)
        self.num: int = None
        self.name: str = None

        self.discontinuous_type:AbstractDiscontinuousType = disc_type
        self.protocol_type = protocol_type

        self.status_comboBox = status_comboBox
        self.disc_widgets = disc_widgets
        self.protocol_comboBox = protocol_comboBox

        self.status_comboBox.currentTextChanged.connect(self.dynamic_check)

    def __str__(self) -> str:
        return "Status {}: {}".format(self.num, self.name)

    def dynamic_check(self, comboBox_text):
        if comboBox_text == self.name:
            self.status_selected.emit(self)
            self.dynamic_change()

    def dynamic_change(self):
        self.discontinuous_type.on_dynamic_change()
        self.protocol_type.on_dynamic_change()

    def setComboBoxVal(self):
        index = self.status_comboBox.findText(self.name)
        self.status_comboBox.setCurrentIndex(index)

class AbstractStatusWifiUI(StatusUI):
    def __init__(self, disc_type: AbstractDiscontinuousType, port_type: AbstractPortType, status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox, udp_widgets) -> None:
        super().__init__(disc_type, ProtocolExtendedUI(protocol_comboBox),status_comboBox, disc_widgets, protocol_comboBox)
        self._port_type = port_type

        self.udp_widgets = udp_widgets

    def dynamic_change(self):
        super().dynamic_change()
        self._port_type.on_dynamic_change()

class StatusTCPContinuous(AbstractStatusWifiUI):
    def __init__(self,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox, udp_widgets) -> None:
        super().__init__(TypeContinuous(disc_widgets), PortTypeTCP(udp_widgets), status_comboBox, disc_widgets, protocol_comboBox, udp_widgets)
        self.num = 21
        self.name = "21 - TCP continuous connection"



class StatusTCPDiscontinuous(AbstractStatusWifiUI):
    def __init__(self,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox, udp_widgets) -> None:
        super().__init__(TypeDiscontinuous(disc_widgets), PortTypeTCP(udp_widgets), status_comboBox, disc_widgets, protocol_comboBox, udp_widgets)
        self.num = 22
        self.name = "22 - TCP discontinuous connection"


class StatusUDP(AbstractStatusWifiUI):
    def __init__(self,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox, udp_widgets) -> None:
        super().__init__(TypeContinuous(disc_widgets), PortTypeUDP(udp_widgets), status_comboBox, disc_widgets, protocol_comboBox, udp_widgets)
        self.num = 23
        self.name = "23 - UDP connection"

class AbstractStatusBluetoothUI(StatusUI):
    def __init__(self, disc_type: AbstractDiscontinuousType,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox) -> None:
        super().__init__(disc_type, ProtocolBaseUI(protocol_comboBox),status_comboBox, disc_widgets, protocol_comboBox)

class StatusBLEContinuous(AbstractStatusBluetoothUI):
    def __init__(self,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox) -> None:
        super().__init__(TypeContinuous(disc_widgets), status_comboBox, disc_widgets, protocol_comboBox)
        self.num = 30
        self.name = "30 - BLE continuous"


class StatusBLEDiscontinuous(AbstractStatusBluetoothUI):
    def __init__(self,  status_comboBox: QComboBox, disc_widgets, protocol_comboBox: QComboBox) -> None:
        super().__init__(TypeDiscontinuous(disc_widgets), status_comboBox, disc_widgets, protocol_comboBox)
        self.num = 31
        self.name = "31 - BLE discontinuous"


class ConfigIntComboBoxUI:
    def __init__(self, input_ui: QComboBox) -> None:
        self.ui_input = input_ui

    def getVal(self):
        return int(self.ui_input.currentText())

    def setVal(self, newVal: int):
        index = self.ui_input.findText(str(newVal))
        self.ui_input.setCurrentIndex(index)

class ConfigSpinBoxUI:
    def __init__(self, input_ui: QSpinBox) -> None:
        self.ui_input = input_ui

    def getVal(self):
        return self.ui_input.value()

    def setVal(self, newVal: int):
        self.ui_input.setProperty("value", newVal)
 

class BasicProtocolsUI:
    def __init__(self, protocol_combobox: QComboBox) -> None:
        self.comboBox = protocol_combobox
        self.names = { "Protocol " + str(i): i for i in range(1,5) }
        self.set_comboBox()
        self.set_item_tooltips()

    def set_comboBox(self):
        self.comboBox.addItems([key for key in self.names])

    def set_item_tooltips(self):
        tooltips = [
            "Sends basic info such as ESP battery level and message timestamp.",
            "Sends ESP basic info and data collected by BME688 (gas, pressure, humidity and temperature sensors).",
            "Sends ESP basic info, data collected by BME688 and the RMS of the vibrations meassured by BMI270.",
            "Sends ESP basic info, data collected by BME688 and BMI270 (frecuency and amplitude of vibrations and their RMS).",
            ]

        for i in range(len(tooltips)):

            self.comboBox.setItemData(i, tooltips[i], QtCore.Qt.ToolTipRole)


class ProtocolBaseUI:
    def __init__(self, protocol_combobox: QComboBox) -> None:
        self.comboBox = protocol_combobox
        self.names = { "Protocol " + str(i): i for i in range(1,5) }
        self.ids = { i: "Protocol " + str(i) for i in range(1,5) }
        self.extra_name = "Protocol 5"
        self.extra_tooltip = "Sends ESP basic info, data collected by BME688 and BMI270 (accelerometer and gyroscope vectors. Warning: huge size)."


    def check_extra_present(self):
        return self.comboBox.findText(self.extra_name)

    def on_dynamic_change(self):
        index = self.check_extra_present()
        if index != -1:
            self.comboBox.removeItem(index)

    def getVal(self):
        text = self.comboBox.currentText()
        return self.names.get(text)

    def setVal(self, newVal: int):
        index = self.comboBox.findText(self.ids[newVal])
        self.comboBox.setCurrentIndex(index)
        

class ProtocolExtendedUI(ProtocolBaseUI):
    def __init__(self, protocol_combobox: QComboBox) -> None:
        super().__init__(protocol_combobox)
        self.names[self.extra_name] = 5
        self.ids[5] = self.extra_name

    def on_dynamic_change(self):
        index = self.check_extra_present()
        if index == -1:
            index = self.comboBox.count()
            self.comboBox.insertItem(index, self.extra_name)
            self.comboBox.setItemData(index, self.extra_tooltip, QtCore.Qt.ToolTipRole)



class StatusConfigUI:
    attrs = ["discontinuous_time_ui", "acc_sampling_ui", "acc_sensibility_ui", "gyro_sensibility_ui", "bme668_sampling_ui"]

    def __init__(self, ui_status: esp_config_win.Ui_Dialog_esp_config , ui_wifi: esp_wifi_config.Ui_Form_wifi_config,status_properties: ConfigProperties):
        self.ui_status = ui_status
        self.ui_wifi = ui_wifi
        self.status_properties = status_properties
        self.protocols_ui = BasicProtocolsUI(self.ui_status.comboBox_protocol)

        self.actual_status: StatusUI = None
        self.discontinuous_time_ui = ConfigSpinBoxUI(self.ui_status.spinBox_disc_time)
        self.acc_sampling_ui = ConfigIntComboBoxUI(self.ui_status.comboBox_acc_sampling)
        self.acc_sensibility_ui = ConfigIntComboBoxUI(self.ui_status.comboBox_acc_sensibility)
        self.gyro_sensibility_ui = ConfigIntComboBoxUI(self.ui_status.comboBox_gyro_sensibility)
        self.bme668_sampling_ui = ConfigIntComboBoxUI(self.ui_status.comboBox_bme_sampling)

        self.wifi_statuses = { 
            item.num: item 
            for item in [class_name(
                self.ui_status.comboBox_conf_status, 
                [self.ui_status.label_disc_time, self.ui_status.spinBox_disc_time],
                self.ui_status.comboBox_protocol,
                [ui_wifi.label_udp_port, ui_wifi.spinBox_udp_port]) 
            for class_name in [StatusTCPContinuous, StatusTCPDiscontinuous, StatusUDP]]}
        self.bluetooth_statuses = { 
            item.num: item 
            for item in [class_name(
                self.ui_status.comboBox_conf_status, 
                [self.ui_status.label_disc_time, self.ui_status.spinBox_disc_time],
                self.ui_status.comboBox_protocol ) 
            for class_name in [StatusBLEContinuous, StatusBLEDiscontinuous]]}

        self.ui_status.pushButton_send_wifi.clicked.connect(self.set_statuses_wifi)
        self.ui_status.pushButton_send_bluetooth.clicked.connect(self.set_statuses_bluetooth)

        for key in self.wifi_statuses:
            self.wifi_statuses[key].status_selected.connect(self.update_actual_status)
        for key in self.bluetooth_statuses:
            self.bluetooth_statuses[key].status_selected.connect(self.update_actual_status)

        self.ui_status.buttonBox_esp_config_confirm.accepted.connect(self.save_ui_into_properties)

    def update_actual_status(self, status_obj):
        self.actual_status = status_obj
        print(self.actual_status)

    def set_statuses_wifi(self):
        self.ui_status.comboBox_conf_status.clear()
        self.ui_status.comboBox_conf_status.addItems([self.wifi_statuses[key].name for key in self.wifi_statuses])
    
    def set_statuses_bluetooth(self):
        self.ui_status.comboBox_conf_status.clear()
        self.ui_status.comboBox_conf_status.addItems([self.bluetooth_statuses[key].name for key in self.bluetooth_statuses])

    def set_actual_status(self, status_id):
        status = self.wifi_statuses.get(status_id)
        if status:
            self.set_statuses_wifi()
            self.ui_status.pushButton_send_wifi.setChecked(True)
            self.actual_status = status
            self.actual_status.setComboBoxVal()
        else:
            status = self.bluetooth_statuses.get(status_id)
            if status:
                self.set_statuses_bluetooth()
                self.ui_status.pushButton_send_bluetooth.setChecked(True)
                self.actual_status = status
                self.actual_status.setComboBoxVal()

    def get_all_ui_values(self):
        res = [self.actual_status.num]
        res.append(self.actual_status.protocol_type.getVal())
        res.extend([getattr(self, attr).getVal() for attr in self.attrs])
        return res

    def set_all_ui_values(self, *vals):
        assert len(vals) == len(self.attrs)+2
        self.set_actual_status(vals[0])
        self.actual_status.protocol_type.setVal(vals[1])
        for i in range(len(self.attrs)):
            attr = self.attrs[i]
            getattr(self, attr).setVal(vals[i+2])

    def save_ui_into_properties(self):
        self.status_properties.set_all(*self.get_all_ui_values())

    def load_from_properties_into_ui(self):
        self.set_all_ui_values(*self.status_properties.get_all())



w = WifiProperties()

w.ssid_changed.connect(lambda port:print("changed!", port))
w.host_invalidated.connect(lambda: print("is"))
w.tcp_invalidated.connect(lambda: print("the"))
w.udp_invalidated.connect(lambda: print("nut"))
w.ssid_invalidated.connect(lambda: print("shack"))
w.passwd_invalidated.connect(lambda: print("!!!"))

w.host_ipv4 = "123.42.56.1111"
w.port_tcp = 100000
w.port_udp = 100000
w.ssid = "lara"
w.ssid = ""
print(w.ssid)

#endregion


class ListsMachine:
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, widget_active_list_parent: QWidget, list_active_layout: QLayout) -> None:
        self.num_found  = 0
        self.num_active = 0
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout
        self.widget_active_list_parent = widget_active_list_parent
        self.active_list_layout = list_active_layout

        self.machine = QStateMachine()
        state_parallel = QState(childMode=QState.ChildMode.ParallelStates, parent=self.machine)

        state_emptiness = QState(state_parallel)
        state_adding = QState(state_parallel)

        state_found_empty = QState(state_emptiness)
        state_found_filled = QState(state_emptiness)
        state_active_empty = QState(state_adding)
        state_active_filled = QState(state_adding)

        # transitions

        trans_found_empty_to_filled = ESPAddFoundTransition(self, self.widget_list_parent, self.list_layout)
        trans_found_empty_to_filled.setTargetState(state_found_filled)
        state_found_empty.addTransition(trans_found_empty_to_filled)

        trans_found_to_found = ESPAddFoundTransition(self, self.widget_list_parent, self.list_layout)
        state_found_filled.addTransition(trans_found_to_found)

        trans_active_empty_to_filled = ESPAddActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        trans_active_empty_to_filled.setTargetState(state_active_filled)
        state_active_empty.addTransition(trans_active_empty_to_filled)

        trans_active_to_active = ESPAddActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        state_active_filled.addTransition(trans_active_to_active)

        trans_found_filled_to_empty = ESPRemoveFoundTransition(self, self.widget_list_parent, self.list_layout)
        trans_found_filled_to_empty.setTargetState(state_found_empty)
        state_found_filled.addTransition(trans_found_filled_to_empty)

        trans_active_filled_to_empty = ESPRemoveActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        trans_active_filled_to_empty.setTargetState(state_active_empty)
        state_active_filled.addTransition(trans_active_filled_to_empty)

        state_emptiness.setInitialState(state_found_empty)
        state_adding.setInitialState(state_active_empty)

        self.machine.setInitialState(state_parallel)
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

    def remove_esp(self, esp_id) -> None:
        try:
            self.mutex.acquire()
            if esp_id in self.esp_dict.keys():
                self.esp_dict.pop(esp_id)
        finally:
            self.mutex.release()




class ESPConfig:
    def __init__(self, esp: "ESP") -> None:
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
        state_config_wifi = QState(state_configs)
        state_config_no_wifi = QState(state_configs)
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

        state_no_config.entered.connect(self.wifi_ui.set_ui_to_default_view)

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

        def _check_valid_connections():
            if self.config_wifi is None or self.send_wifi is None:
                self.machine.postEvent(UnableToSendEvent())
            else:
                self.machine.postEvent(AbleToSendEvent())

        state_config_wifi.entered.connect(_auto_show_toolbar)
        state_config_no_wifi.entered.connect(_auto_hide_toolbar)

        state_config_wifi.entered.connect(_check_valid_connections)
        state_config_no_wifi.entered.connect(_check_valid_connections)
        
        trans_wifi_to_error = InvalidWifiConfigTransition()
        trans_wifi_to_error.setTargetState(state_wifi_error)
        state_config_wifi.addTransition(trans_wifi_to_error)

        for signal in self.wifi_ui.get_signals():
            trans_wifi_error = QSignalTransition(signal)
            trans_wifi_error.setTargetState(state_wifi_error)
            state_wifi_error.addTransition(trans_wifi_error)

        trans_error_to_wifi = ValidWifiConfigTransition()
        trans_error_to_wifi.setTargetState(state_config_wifi)
        state_wifi_error.addTransition(trans_error_to_wifi)

        def _check_valid_wifi():
            print("checking stuff")
            result = self.wifi_properties.validate_all(*self.wifi_ui.get_all_ui_values())
            self.wifi_properties.set_all(*self.wifi_ui.get_all_ui_values())
            if result:
                self.machine.postEvent(ValidWifiConfigEvent())
                self.machine.postEvent(AbleToSendEvent())

        state_wifi_error.entered.connect(_check_valid_wifi)


        def _on_start_click():
            result = self.wifi_properties.validate_all(*self.wifi_ui.get_all_ui_values())
            if result:
                self.esp.machine.postEvent(SendStartEvent())
            else:
                self.machine.postEvent(InvalidWifiConfigEvent())
                self.machine.postEvent(UnableToSendEvent())

        self.esp.ui_active.pushButton_esp_active_restart.clicked.connect(_on_start_click)

        self.machine.start()
    

class startButtonUI:
    def __init__(self, button_start: QPushButton) -> None:
        self.ui_button = button_start

        icon_play = QtGui.QIcon()
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.icon_play = icon_play

        icon_restart = QtGui.QIcon()
        icon_restart
        
        self.ui_button.setIcon(icon_play)      
    



class ESP:
    def __init__(self, esp_id, esp_mac, esp_lists_machine: ListsMachine, esp_dict_list: "ESPDicts", main_win) -> None:
        self.esp_id = esp_id
        self.esp_mac = esp_mac
        self.machine: QStateMachine = None
        self.esp_lists_machine: ListsMachine = esp_lists_machine
        self.esp_dict = esp_dict_list
        self.main_win = main_win

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


        trans_make_active = ESPFoundTransition(self.esp_dict)
        trans_make_active.setTargetState(state_activo)
        state_dead.addTransition(trans_make_active)

        trans_begin_send = SendStartTransition()
        trans_begin_send.setTargetState(state_proceso_envio)
        state_activo.addTransition(trans_begin_send)

        state_configurando.entered.connect()


        state_proceso_envio.setInitialState(state_configurando)
        self.machine.setInitialState(state_encontrado)
        self.machine.start()

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


    def set_found_widget(self) -> QFrame:
        ui_found = esp_found_item.Ui_Form_esp_found_item()
        found_frame = QFrame()
        ui_found.setupUi(found_frame)
        self.add_btn = ui_found.pushButton_esp_found_add
        self.found_widget = found_frame

        self.add_btn.clicked.connect(self._found_to_active_slot)

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
    def __init__(self, plot_id, plot_list: PlotListsMachine, plot_manager: "LivePlotManager") -> None:
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

class LivePlotManager:
    def __init__(self, ui_main: main_display.Ui_MainWindow) -> None:
        self.plot_list = PlotListsMachine(
            ui_main_disp.scrollAreaWidgetContents_added_plots, 
            ui_main_disp.verticalLayout_added_plots_list,
            ui_main.stackedWidget_plot_count)
        self.ui_main = ui_main
        self.live_plots = dict()

        ui_main.pushButton_add_live_plot.clicked.connect(self.add_new_plot)

    def add_new_plot(self):
        new_plot = LivePlot(self.plot_list.num_plots, self.plot_list, self)
        self.live_plots[self.plot_list.num_plots] = new_plot
        self.plot_list.machine.postEvent(LivePlotAddEvent(new_plot.plot_frame))




    

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

    plot_manager = LivePlotManager(ui_main_disp)


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



    #ui_main_disp.pushButton_search_refresh.clicked.connect(add_active_item)

    def add_live_plot():
        ui_plot = live_plot.Ui_Form_live_plot()
        plot_frame = QFrame()
        ui_plot.setupUi(plot_frame)
        ui_main_disp.verticalLayout_added_plots_list.addWidget(plot_frame)

    #ui_main_disp.pushButton_add_live_plot.clicked.connect(add_live_plot)

    window.show()
    debug_dialog.show()
    machine_buscando.start()

    sys.exit(app.exec())