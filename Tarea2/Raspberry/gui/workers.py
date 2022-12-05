from PyQt5.QtCore import QObject, pyqtSignal
import typing



class Worker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, slot, *slot_args, parent: typing.Optional['QObject'] = None) -> None:
        super().__init__(parent)
        self.slot = slot
        self.slot_args = slot_args

    def process(self):
        print("henno")
        try:
            print("trabajanding")
            self.slot(*self.slot_args)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

