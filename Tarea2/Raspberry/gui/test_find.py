
from queue import Queue
from multiprocessing import Process, Lock

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel, QWidget, QLayout, QSpinBox, QLineEdit, QComboBox, QStackedWidget, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QStateMachine, QState, QFinalState, QAbstractTransition, QEventTransition, pyqtProperty, pyqtSignal, QSignalTransition, pyqtBoundSignal
import typing

from gui.forms import main_display, esp_found_item, esp_active_item,  esp_wifi_config, esp_config_win, live_plot


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()

    


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


    ## machinery

    

    

    def post_ev():
        esp_dict_list.esp_dict[1110].machine.postEvent(ESPSendingEvent())

    ## Buttons signals
    btn_end_find.clicked.connect(lambda: machine_buscando.postEvent(EndFindEvent()))
    esp_1_btn_found.clicked.connect(lambda: machine_buscando.postEvent(ESPFoundEvent(1110, "aa-bb-cc-dd-ee-ff")))
    esp_2_btn_found.clicked.connect(post_ev)
    esp_3_btn_found.clicked.connect(lambda: esp_dict_list.esp_dict[1110].machine.postEvent(ESPSleepingEvent()))



    #ui_main_disp.pushButton_search_refresh.clicked.connect(add_active_item)
    window.show()
    debug_dialog.show()

    sys.exit(app.exec())