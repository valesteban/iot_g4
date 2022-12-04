from PyQt5.QtCore import QEvent


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
    def __init__(self, should_transition) -> None:
        super().__init__(self.EVENT_TYPE)
        self.should_transition = should_transition

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

class ESPConfiguringEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+17
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPSendingEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+18
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPSleepingEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+19
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)

class ESPErroringEvent(QEvent):
    EVENT_TYPE = QEvent.Type.User+20
    def __init__(self) -> None:
        super().__init__(self.EVENT_TYPE)