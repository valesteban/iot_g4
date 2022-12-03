# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/malva/esp/iot_g4/Tarea2/Raspberry/extra/qt/esp_config_win.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_esp_config(object):
    def setupUi(self, Dialog_esp_config):
        Dialog_esp_config.setObjectName("Dialog_esp_config")
        Dialog_esp_config.resize(400, 476)
        self.verticalLayout_esp_config = QtWidgets.QVBoxLayout(Dialog_esp_config)
        self.verticalLayout_esp_config.setObjectName("verticalLayout_esp_config")
        self.frame_esp_config_protocols = QtWidgets.QFrame(Dialog_esp_config)
        self.frame_esp_config_protocols.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_esp_config_protocols.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_esp_config_protocols.setObjectName("frame_esp_config_protocols")
        self.verticalLayout_esp_config_protocols = QtWidgets.QVBoxLayout(self.frame_esp_config_protocols)
        self.verticalLayout_esp_config_protocols.setObjectName("verticalLayout_esp_config_protocols")
        self.groupBox_send_medium = QtWidgets.QGroupBox(self.frame_esp_config_protocols)
        self.groupBox_send_medium.setObjectName("groupBox_send_medium")
        self.horizontalLayout_send_medium = QtWidgets.QHBoxLayout(self.groupBox_send_medium)
        self.horizontalLayout_send_medium.setObjectName("horizontalLayout_send_medium")
        self.pushButton_send_bluetooth = QtWidgets.QPushButton(self.groupBox_send_medium)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_bluetooth/images/bluetooth.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon_bluetooth/images/bluetooth_active.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.pushButton_send_bluetooth.setIcon(icon)
        self.pushButton_send_bluetooth.setCheckable(True)
        self.pushButton_send_bluetooth.setAutoRepeat(False)
        self.pushButton_send_bluetooth.setAutoExclusive(True)
        self.pushButton_send_bluetooth.setObjectName("pushButton_send_bluetooth")
        self.horizontalLayout_send_medium.addWidget(self.pushButton_send_bluetooth)
        self.pushButton_send_wifi = QtWidgets.QPushButton(self.groupBox_send_medium)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon_wifi/images/wifi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon_wifi/images/wifi_active.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.pushButton_send_wifi.setIcon(icon1)
        self.pushButton_send_wifi.setCheckable(True)
        self.pushButton_send_wifi.setAutoExclusive(True)
        self.pushButton_send_wifi.setObjectName("pushButton_send_wifi")
        self.horizontalLayout_send_medium.addWidget(self.pushButton_send_wifi)
        self.verticalLayout_esp_config_protocols.addWidget(self.groupBox_send_medium)
        self.gridLayout_protocol_params = QtWidgets.QGridLayout()
        self.gridLayout_protocol_params.setObjectName("gridLayout_protocol_params")
        self.comboBox_conf_status = QtWidgets.QComboBox(self.frame_esp_config_protocols)
        self.comboBox_conf_status.setObjectName("comboBox_conf_status")
        self.gridLayout_protocol_params.addWidget(self.comboBox_conf_status, 0, 1, 1, 1)
        self.spinBox_disc_time = QtWidgets.QSpinBox(self.frame_esp_config_protocols)
        self.spinBox_disc_time.setAccelerated(True)
        self.spinBox_disc_time.setMinimum(10)
        self.spinBox_disc_time.setMaximum(3600)
        self.spinBox_disc_time.setObjectName("spinBox_disc_time")
        self.gridLayout_protocol_params.addWidget(self.spinBox_disc_time, 1, 1, 1, 1)
        self.label_conf_status = QtWidgets.QLabel(self.frame_esp_config_protocols)
        self.label_conf_status.setObjectName("label_conf_status")
        self.gridLayout_protocol_params.addWidget(self.label_conf_status, 0, 0, 1, 1)
        self.label_disc_time = QtWidgets.QLabel(self.frame_esp_config_protocols)
        self.label_disc_time.setObjectName("label_disc_time")
        self.gridLayout_protocol_params.addWidget(self.label_disc_time, 1, 0, 1, 1)
        self.label_protocol = QtWidgets.QLabel(self.frame_esp_config_protocols)
        self.label_protocol.setObjectName("label_protocol")
        self.gridLayout_protocol_params.addWidget(self.label_protocol, 2, 0, 1, 1)
        self.comboBox_protocol = QtWidgets.QComboBox(self.frame_esp_config_protocols)
        self.comboBox_protocol.setObjectName("comboBox_protocol")
        self.gridLayout_protocol_params.addWidget(self.comboBox_protocol, 2, 1, 1, 1)
        self.verticalLayout_esp_config_protocols.addLayout(self.gridLayout_protocol_params)
        self.verticalLayout_esp_config.addWidget(self.frame_esp_config_protocols)
        self.frame_esp_params = QtWidgets.QFrame(Dialog_esp_config)
        self.frame_esp_params.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_esp_params.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_esp_params.setObjectName("frame_esp_params")
        self.verticalLayout_esp_params = QtWidgets.QVBoxLayout(self.frame_esp_params)
        self.verticalLayout_esp_params.setObjectName("verticalLayout_esp_params")
        self.label_esp_params = QtWidgets.QLabel(self.frame_esp_params)
        self.label_esp_params.setObjectName("label_esp_params")
        self.verticalLayout_esp_params.addWidget(self.label_esp_params)
        self.gridLayout_esp_params = QtWidgets.QGridLayout()
        self.gridLayout_esp_params.setObjectName("gridLayout_esp_params")
        self.label_acc_sensibility = QtWidgets.QLabel(self.frame_esp_params)
        self.label_acc_sensibility.setObjectName("label_acc_sensibility")
        self.gridLayout_esp_params.addWidget(self.label_acc_sensibility, 1, 0, 1, 1)
        self.label_gyro_sensibility = QtWidgets.QLabel(self.frame_esp_params)
        self.label_gyro_sensibility.setObjectName("label_gyro_sensibility")
        self.gridLayout_esp_params.addWidget(self.label_gyro_sensibility, 2, 0, 1, 1)
        self.label_acc_sampling = QtWidgets.QLabel(self.frame_esp_params)
        self.label_acc_sampling.setObjectName("label_acc_sampling")
        self.gridLayout_esp_params.addWidget(self.label_acc_sampling, 0, 0, 1, 1)
        self.label_bme_sampling = QtWidgets.QLabel(self.frame_esp_params)
        self.label_bme_sampling.setObjectName("label_bme_sampling")
        self.gridLayout_esp_params.addWidget(self.label_bme_sampling, 3, 0, 1, 1)
        self.comboBox_acc_sampling = QtWidgets.QComboBox(self.frame_esp_params)
        self.comboBox_acc_sampling.setObjectName("comboBox_acc_sampling")
        self.comboBox_acc_sampling.addItem("")
        self.comboBox_acc_sampling.addItem("")
        self.comboBox_acc_sampling.addItem("")
        self.comboBox_acc_sampling.addItem("")
        self.gridLayout_esp_params.addWidget(self.comboBox_acc_sampling, 0, 1, 1, 1)
        self.comboBox_acc_sensibility = QtWidgets.QComboBox(self.frame_esp_params)
        self.comboBox_acc_sensibility.setObjectName("comboBox_acc_sensibility")
        self.comboBox_acc_sensibility.addItem("")
        self.comboBox_acc_sensibility.addItem("")
        self.comboBox_acc_sensibility.addItem("")
        self.comboBox_acc_sensibility.addItem("")
        self.gridLayout_esp_params.addWidget(self.comboBox_acc_sensibility, 1, 1, 1, 1)
        self.comboBox_gyro_sensibility = QtWidgets.QComboBox(self.frame_esp_params)
        self.comboBox_gyro_sensibility.setObjectName("comboBox_gyro_sensibility")
        self.comboBox_gyro_sensibility.addItem("")
        self.comboBox_gyro_sensibility.addItem("")
        self.comboBox_gyro_sensibility.addItem("")
        self.gridLayout_esp_params.addWidget(self.comboBox_gyro_sensibility, 2, 1, 1, 1)
        self.comboBox_bme_sampling = QtWidgets.QComboBox(self.frame_esp_params)
        self.comboBox_bme_sampling.setObjectName("comboBox_bme_sampling")
        self.comboBox_bme_sampling.addItem("")
        self.comboBox_bme_sampling.addItem("")
        self.comboBox_bme_sampling.addItem("")
        self.comboBox_bme_sampling.addItem("")
        self.gridLayout_esp_params.addWidget(self.comboBox_bme_sampling, 3, 1, 1, 1)
        self.verticalLayout_esp_params.addLayout(self.gridLayout_esp_params)
        self.verticalLayout_esp_config.addWidget(self.frame_esp_params)
        self.buttonBox_esp_config_confirm = QtWidgets.QDialogButtonBox(Dialog_esp_config)
        self.buttonBox_esp_config_confirm.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_esp_config_confirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_esp_config_confirm.setObjectName("buttonBox_esp_config_confirm")
        self.verticalLayout_esp_config.addWidget(self.buttonBox_esp_config_confirm)

        self.retranslateUi(Dialog_esp_config)
        self.buttonBox_esp_config_confirm.accepted.connect(Dialog_esp_config.accept)
        self.buttonBox_esp_config_confirm.rejected.connect(Dialog_esp_config.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_esp_config)

    def retranslateUi(self, Dialog_esp_config):
        _translate = QtCore.QCoreApplication.translate
        Dialog_esp_config.setWindowTitle(_translate("Dialog_esp_config", "Dialog"))
        self.groupBox_send_medium.setTitle(_translate("Dialog_esp_config", "Data transfer medium"))
        self.pushButton_send_bluetooth.setText(_translate("Dialog_esp_config", "Bluetooth"))
        self.pushButton_send_wifi.setText(_translate("Dialog_esp_config", "Wi-Fi"))
        self.label_conf_status.setText(_translate("Dialog_esp_config", "Configuration Status"))
        self.label_disc_time.setText(_translate("Dialog_esp_config", "Discontinuos Time (s)"))
        self.label_protocol.setText(_translate("Dialog_esp_config", "Protocol"))
        self.label_esp_params.setText(_translate("Dialog_esp_config", "ESP-32 Parameters"))
        self.label_acc_sensibility.setText(_translate("Dialog_esp_config", "Acc Sensibility"))
        self.label_gyro_sensibility.setText(_translate("Dialog_esp_config", "Gyro Sensibility"))
        self.label_acc_sampling.setText(_translate("Dialog_esp_config", "Acc Sampling"))
        self.label_bme_sampling.setText(_translate("Dialog_esp_config", "BME688 Sampling"))
        self.comboBox_acc_sampling.setItemText(0, _translate("Dialog_esp_config", "10"))
        self.comboBox_acc_sampling.setItemText(1, _translate("Dialog_esp_config", "100"))
        self.comboBox_acc_sampling.setItemText(2, _translate("Dialog_esp_config", "400"))
        self.comboBox_acc_sampling.setItemText(3, _translate("Dialog_esp_config", "1000"))
        self.comboBox_acc_sensibility.setItemText(0, _translate("Dialog_esp_config", "2"))
        self.comboBox_acc_sensibility.setItemText(1, _translate("Dialog_esp_config", "4"))
        self.comboBox_acc_sensibility.setItemText(2, _translate("Dialog_esp_config", "8"))
        self.comboBox_acc_sensibility.setItemText(3, _translate("Dialog_esp_config", "16"))
        self.comboBox_gyro_sensibility.setItemText(0, _translate("Dialog_esp_config", "200"))
        self.comboBox_gyro_sensibility.setItemText(1, _translate("Dialog_esp_config", "250"))
        self.comboBox_gyro_sensibility.setItemText(2, _translate("Dialog_esp_config", "500"))
        self.comboBox_bme_sampling.setItemText(0, _translate("Dialog_esp_config", "1"))
        self.comboBox_bme_sampling.setItemText(1, _translate("Dialog_esp_config", "2"))
        self.comboBox_bme_sampling.setItemText(2, _translate("Dialog_esp_config", "3"))
        self.comboBox_bme_sampling.setItemText(3, _translate("Dialog_esp_config", "4"))
from . import icons_rc
