from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QWidget, QSpinBox, QLineEdit

from gui.properties import WifiProperties
from gui.forms import esp_wifi_config



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
