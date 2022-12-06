import traceback as tb
from PyQt5.QtWidgets import QMessageBox

class ErrorMessage:
    def __init__(self, win_parent = None) -> None:
        self.parent = win_parent

    def launch_exception_message(self, e_instance, icon: QMessageBox.Icon, win_title: str, msg_body: str):
        qmsg = QMessageBox(
            icon, 
            win_title, 
            msg_body, 
            buttons=QMessageBox.StandardButton.Ok,
            parent=self.parent)
        qmsg.setDetailedText(''.join(tb.format_exception(None, e_instance, e_instance.__traceback__)))
        qmsg.exec()

    def launch_critical_exception_message(self, e_instance, win_title: str, msg_body: str = "An error has occurred. You cannot go back."):
        self.launch_exception_message(e_instance, QMessageBox.Icon.Critical, win_title, msg_body)

    def launch_warning_exception_message(self, e_instance, win_title: str, msg_body: str = "An error has occurred. You were wrong. Go back."):
        self.launch_exception_message(e_instance, QMessageBox.Icon.Warning, win_title, msg_body)