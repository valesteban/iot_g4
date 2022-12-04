from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel
from PyQt5 import QtWidgets

from gui.rasp import Rasp, Controller
from gui.all_events import ESPSendingEvent, ESPSleepingEvent, EndFindEvent, ESPFoundEvent

from db_manager import change_db_config, return_db_config


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()


    controller = Controller(change_db_config, return_db_config)
    rasp = Rasp(window, controller)

    debug_dialog = QDialog(window)
    verticalLayout_debug= QtWidgets.QVBoxLayout(debug_dialog)

    esp_found_label = QLabel("Found window", debug_dialog)
    btn_end_find = QPushButton("End find", debug_dialog)
    esp_1_label = QtWidgets.QLabel("ESP1", debug_dialog)
    esp_1_btn_found = QtWidgets.QPushButton("found", debug_dialog)
    esp_2_btn_found = QtWidgets.QPushButton("sending", debug_dialog)
    esp_3_btn_found = QtWidgets.QPushButton("sleeping", debug_dialog)
    esp_4_btn_found = QtWidgets.QPushButton("error", debug_dialog)

    verticalLayout_debug.addWidget(esp_found_label)
    verticalLayout_debug.addWidget(btn_end_find)
    verticalLayout_debug.addWidget(esp_1_label)
    verticalLayout_debug.addWidget(esp_1_btn_found)
    verticalLayout_debug.addWidget(esp_2_btn_found)
    verticalLayout_debug.addWidget(esp_3_btn_found)
    verticalLayout_debug.addWidget(esp_4_btn_found)

    def post_ev():
        rasp.esp_dict_list.esp_dict[1110].machine.postEvent(ESPSendingEvent())

    ## Buttons signals
    btn_end_find.clicked.connect(lambda: rasp.device_search.machine.postEvent(EndFindEvent()))
    esp_1_btn_found.clicked.connect(lambda: rasp.device_search.machine.postEvent(ESPFoundEvent(1110, "aa-bb-cc-dd-ee-ff")))
    esp_2_btn_found.clicked.connect(post_ev)
    esp_3_btn_found.clicked.connect(lambda: rasp.esp_dict_list.esp_dict[1110].machine.postEvent(ESPSleepingEvent()))

    window.show()
    debug_dialog.show()

    sys.exit(app.exec())