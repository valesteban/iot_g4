from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QPushButton



class SendStatusUI:
    _translate = QtCore.QCoreApplication.translate
    def __init__(self, status_icon: QtWidgets.QLabel, status_label, config_method_wifi: bool = True, send_method_wifi: bool = True, status_name: str = "", protocol_name: str = "") -> None:
        self.default_active = QtGui.QPixmap(":/icon_ready/images/check_blue.png")
        self.dead_icon = QtGui.QPixmap(":/icon_ready/images/ghost_grey.png")

        self.wifi_icons = {
            "config": QtGui.QPixmap(":/icon_wifi/images/wifi_active.png"),
            "deepsleep": QtGui.QPixmap(":/icon_wifi/images/wifi_light_blue.png"),
            "send": QtGui.QPixmap(":/icon_wifi/images/wifi_green.png"),
            "error": QtGui.QPixmap(":/icon_wifi/images/wifi_red.png"),
        }

        self.bluetooth_icons = {
            "config": QtGui.QPixmap(":/icon_bluetooth/images/bluetooth_active.png"),
            "deepsleep": QtGui.QPixmap(":/icon_bluetooth/images/bluetooth_light_blue.png"),
            "send": QtGui.QPixmap(":/icon_bluetooth/images/bluetooth_green.png"),
            "error": QtGui.QPixmap(":/icon_bluetooth/images/bluetooth_red.png"),
        }

        self.status_icon = status_icon
        self.status_label = status_label
        self.config_method_wifi = config_method_wifi
        self.send_method_wifi = send_method_wifi
        self.status_name = status_name 
        self.protocol_name = protocol_name

        self.labels_txt = self.update_labels()


    def set_send_parameters(self, config_method_wifi: bool, send_method_wifi: bool, status_name: str, protocol_name: str):
        self.config_method_wifi = config_method_wifi
        self.send_method_wifi = send_method_wifi
        self.status_name = status_name 
        self.protocol_name = protocol_name

        self.labels_txt = self.update_labels()

    def update_labels(self):
        return {
            "config": "Configuring",
            "deepsleep": "Deep Sleep: {} :{}".format(self.status_name, self.protocol_name),
            "send": "Sending: {} :{}".format(self.status_name, self.protocol_name),
            "error": "Error",
            "dead": "Dead"
        }

    def set_send_status(self, mode, configuring = False, extra_msg=""):
        if (configuring and self.config_method_wifi) or (not configuring and self.send_method_wifi):
            self.status_icon.setPixmap(self.wifi_icons[mode])
        else:
            self.status_icon.setPixmap(self.bluetooth_icons[mode])
        
        self.status_label.setText(self._translate("Form_esp_active", self.labels_txt[mode]+extra_msg))

    def set_send_status_default(self):
        self.status_icon.setPixmap(self.default_active)
        self.status_label.setText(self._translate("Form_esp_active", "Active"))

    def set_send_status_config(self):
        self.set_send_status("config", True)

    def set_send_status_send(self):
        self.set_send_status("send")

    def set_send_status_deepsleep(self):
        self.set_send_status("deepsleep")

    def set_send_status_error(self, configuring):
        if configuring:
            extra_msg = " while configuring"
        else:
            extra_msg = " while sending"
        self.set_send_status("error", configuring, extra_msg)

    def set_send_status_dead(self):
        self.status_icon.setPixmap(self.dead_icon)
        self.status_label.setText(self._translate("Form_esp_active", self.labels_txt["dead"]))


class StartButtonUI:
    _translate = QtCore.QCoreApplication.translate

    def __init__(self, button_start: QPushButton) -> None:
        self.ui_button = button_start

        icon_play = QtGui.QIcon()
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon_play.addPixmap(QtGui.QPixmap(":/icon_start/images/play_button_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.icon_play = icon_play

        icon_restart = QtGui.QIcon()
        icon_restart.addPixmap(QtGui.QPixmap(":/icon_restart/images/restart_enabled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_restart.addPixmap(QtGui.QPixmap(":/icon_restart/images/restart_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon_restart.addPixmap(QtGui.QPixmap(":/icon_restart/images/restart_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.icon_restart = icon_restart
         

    def set_start_button(self):
        self.ui_button.setIcon(self.icon_play)  
        self.ui_button.setText(self._translate("Form_esp_active", "Start"))

    def set_restart_button(self):
        self.ui_button.setIcon(self.icon_restart)
        self.ui_button.setText(self._translate("Form_esp_active", "Restart"))
    

class ESPInfo:
    _translate = QtCore.QCoreApplication.translate
    def __init__(self, id_label: QtWidgets.QLabel, mac_label: QtWidgets.QLabel) -> None:
        self.id_label = id_label
        self.mac_label = mac_label
    
    def set_id(self, new_id:str, new_mac:str):
        new_id = str(new_id)
        new_mac = str(new_mac)

        self.id_label.setText(self._translate("Form_esp_active", new_id))
        self.id_label.setText(self._translate("Form_esp_active", new_mac))