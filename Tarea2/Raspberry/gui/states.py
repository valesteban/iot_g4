from PyQt5.QtCore import QState, QEvent
import typing

#from gui.esp_dev import ESPDevice

class FoundState(QState):
    def __init__(self, esp: "ESPDevice", parent: typing.Optional['QState'] = None) -> None:
        super().__init__(parent)
        self.esp = esp

    def onEntry(self, event: QEvent) -> None:
        self.esp.found_widget.setVisible(True)
        return super().onEntry(event)

class WifiState(QState):
    def __init__(self, parent: typing.Optional['QState'] = None) -> None:
        super().__init__(parent)

    def should_send(self, a_bool):
        return a_bool


class NoWifiState(QState):
    def __init__(self, parent: typing.Optional['QState'] = None) -> None:
        super().__init__(parent)

    def should_send(self, a_bool):
        return True