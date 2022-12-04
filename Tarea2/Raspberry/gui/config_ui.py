from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QSpinBox, QComboBox

from gui.forms import esp_wifi_config, esp_config_win
from gui.properties import ConfigProperties
 


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
