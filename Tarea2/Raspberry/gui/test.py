from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDialog
from PyQt5 import QtCore

from forms import main_display, esp_found_item, esp_active_item,  esp_wifi_config, esp_config_win, live_plot


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    ui_main_disp = main_display.Ui_MainWindow()
    ui_main_disp.setupUi(window)

    def add_found_item():
        ui_found = esp_found_item.Ui_Form_esp_found_item()
        found_frame = QFrame()
        ui_found.setupUi(found_frame)
        
        ui_main_disp.verticalLayout_found_list.addWidget(found_frame)

    ui_main_disp.pushButton_search_refresh.clicked.connect(add_found_item)

    def add_active_item():
        ui_wifi = esp_wifi_config.Ui_Form_wifi_config()
        wifi_frame = QFrame()
        ui_wifi.setupUi(wifi_frame)

        ui_active = esp_active_item.Ui_Form_esp_active()
        active_frame = QFrame()
        ui_active.setupUi(active_frame)

        ui_active.verticalLayout_wifi_config_expandable.addWidget(wifi_frame)

        ui_active.toolButton_esp_active_wifi_config.setContent(wifi_frame)

        def open_config_dialog():
            ui_config = esp_config_win.Ui_Dialog_esp_config()
            config_dialog = QDialog(window)
            ui_config.setupUi(config_dialog)
            config_dialog.show()

        ui_main_disp.verticalLayout_active_list.addWidget(active_frame)

        ui_active.pushButton_esp_active_config.clicked.connect(open_config_dialog)



    ui_main_disp.pushButton_search_refresh.clicked.connect(add_active_item)

    def add_live_plot():
        ui_plot = live_plot.Ui_Form_live_plot()
        plot_frame = QFrame()
        ui_plot.setupUi(plot_frame)
        ui_main_disp.verticalLayout_added_plots_list.addWidget(plot_frame)

    ui_main_disp.pushButton_add_live_plot.clicked.connect(add_live_plot)

    window.show()

    sys.exit(app.exec())