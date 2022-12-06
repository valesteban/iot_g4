from PyQt5.QtCore import QObject, pyqtSignal

from gui.error_handling import ErrorMessage
from gui.all_events import EndFindEvent, ESPActiveEvent

import typing
import sys


class Worker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(object)

    def __init__(self, slot, slot_args=[], parent: typing.Optional['QObject'] = None) -> None:
        super().__init__(parent)
        self.slot = slot
        self.slot_args = slot_args

    def process(self):
        try:
            print(self.__class__, "is working rn")
            self.slot(*self.slot_args)
            self.finished.emit()
        except Exception as e:
            self.error.emit(e)

    def setup_thread(self, thread):
        self.moveToThread(thread)
        self.error.connect(self.on_error)
        thread.started.connect(self.process)
        self.finished.connect(thread.quit)
        #self.finished.connect(self.deleteLater)
        thread.finished.connect(thread.deleteLater)

    def on_error(self, error_instance):
        print(error_instance, file=sys.stderr)

class FindESPWorker(Worker):
    def __init__(self, window_parent, caller, slot, slot_args=[], parent: typing.Optional['QObject'] = None) -> None:
        super().__init__(slot, slot_args, parent)
        self.window_parent = window_parent
        self.caller = caller
        self.error_msg = ErrorMessage(self.window_parent)

    def on_error(self, error_instance):
        super().on_error(error_instance)
        self.error_msg.launch_warning_exception_message(error_instance, "ESP Seach Error", "An error occurred during the search of an ESP device.\nClose this message and try again.")
        self.caller.machine.postEvent(EndFindEvent())

class ConfigESPBLEWorker(Worker):
    def __init__(self, window_parent, caller, slot, slot_args=[], parent: typing.Optional['QObject'] = None) -> None:
        super().__init__(slot, slot_args, parent)
        self.window_parent = window_parent
        self.caller = caller
        self.error_msg = ErrorMessage(self.window_parent)

    def on_error(self, error_instance):
        super().on_error(error_instance)
        self.error_msg.launch_critical_exception_message(error_instance,"BLE conf error", "A fatal error has occurred while configuring the ESP through BLE.\nSend process has been stopped.")
        self.caller.machine.postEvent(ESPActiveEvent())
        self.caller.send_status.set_send_status_error(configuring=True, extra_msg=". Configuración cancelada")

class ConfigESPWifiWorker(Worker):
    def __init__(self, window_parent, caller, slot, slot_args=[], parent: typing.Optional['QObject'] = None) -> None:
        super().__init__(slot, slot_args, parent)
        self.window_parent = window_parent
        self.caller = caller
        self.error_msg = ErrorMessage(self.window_parent)

    def on_error(self, error_instance):
        super().on_error(error_instance)
        self.error_msg.launch_critical_exception_message(error_instance,"Wifi conf error", "A fatal error has occurred while configuring the ESP through Wifi.\nSend process has been stopped.")
        self.caller.machine.postEvent(ESPActiveEvent())
        self.caller.send_status.set_send_status_error(configuring=True, extra_msg=". Configuración cancelada")

    