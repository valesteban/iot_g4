# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Users\valeg\Documents\IoT\iot_g4\Tarea2\Raspberry\extra\qt\esp_wifi_config.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_wifi_config(object):
    def setupUi(self, Form_wifi_config):
        Form_wifi_config.setObjectName("Form_wifi_config")
        Form_wifi_config.resize(731, 178)
        self.verticalLayout_wifi_config = QtWidgets.QVBoxLayout(Form_wifi_config)
        self.verticalLayout_wifi_config.setObjectName("verticalLayout_wifi_config")
        self.gridLayout_wifi_config = QtWidgets.QGridLayout()
        self.gridLayout_wifi_config.setHorizontalSpacing(15)
        self.gridLayout_wifi_config.setVerticalSpacing(2)
        self.gridLayout_wifi_config.setObjectName("gridLayout_wifi_config")
        self.label_udp_port_status_msg = QtWidgets.QLabel(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_udp_port_status_msg.sizePolicy().hasHeightForWidth())
        self.label_udp_port_status_msg.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_udp_port_status_msg.setPalette(palette)
        self.label_udp_port_status_msg.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_udp_port_status_msg.setObjectName("label_udp_port_status_msg")
        self.gridLayout_wifi_config.addWidget(self.label_udp_port_status_msg, 2, 3, 1, 1)
        self.label_host_ip = QtWidgets.QLabel(Form_wifi_config)
        self.label_host_ip.setObjectName("label_host_ip")
        self.gridLayout_wifi_config.addWidget(self.label_host_ip, 1, 0, 1, 1)
        self.label_pass = QtWidgets.QLabel(Form_wifi_config)
        self.label_pass.setObjectName("label_pass")
        self.gridLayout_wifi_config.addWidget(self.label_pass, 5, 2, 1, 1)
        self.label_ssid = QtWidgets.QLabel(Form_wifi_config)
        self.label_ssid.setObjectName("label_ssid")
        self.gridLayout_wifi_config.addWidget(self.label_ssid, 5, 0, 1, 1)
        self.label_tcp_port_status_msg = QtWidgets.QLabel(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_tcp_port_status_msg.sizePolicy().hasHeightForWidth())
        self.label_tcp_port_status_msg.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_tcp_port_status_msg.setPalette(palette)
        self.label_tcp_port_status_msg.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_tcp_port_status_msg.setObjectName("label_tcp_port_status_msg")
        self.gridLayout_wifi_config.addWidget(self.label_tcp_port_status_msg, 2, 1, 1, 1)
        self.label_pass_status_msg = QtWidgets.QLabel(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_pass_status_msg.sizePolicy().hasHeightForWidth())
        self.label_pass_status_msg.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_pass_status_msg.setPalette(palette)
        self.label_pass_status_msg.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_pass_status_msg.setObjectName("label_pass_status_msg")
        self.gridLayout_wifi_config.addWidget(self.label_pass_status_msg, 4, 3, 1, 1)
        self.label_host_ip_status_msg = QtWidgets.QLabel(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_host_ip_status_msg.sizePolicy().hasHeightForWidth())
        self.label_host_ip_status_msg.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label_host_ip_status_msg.setPalette(palette)
        self.label_host_ip_status_msg.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_host_ip_status_msg.setObjectName("label_host_ip_status_msg")
        self.gridLayout_wifi_config.addWidget(self.label_host_ip_status_msg, 0, 1, 1, 1)
        self.label_tcp_port = QtWidgets.QLabel(Form_wifi_config)
        self.label_tcp_port.setObjectName("label_tcp_port")
        self.gridLayout_wifi_config.addWidget(self.label_tcp_port, 3, 0, 1, 1)
        self.lineEdit_pass = QtWidgets.QLineEdit(Form_wifi_config)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pass.setObjectName("lineEdit_pass")
        self.gridLayout_wifi_config.addWidget(self.lineEdit_pass, 5, 3, 1, 1)
        self.label_udp_port = QtWidgets.QLabel(Form_wifi_config)
        self.label_udp_port.setObjectName("label_udp_port")
        self.gridLayout_wifi_config.addWidget(self.label_udp_port, 3, 2, 1, 1)
        self.lineEdit_ssid = QtWidgets.QLineEdit(Form_wifi_config)
        self.lineEdit_ssid.setObjectName("lineEdit_ssid")
        self.gridLayout_wifi_config.addWidget(self.lineEdit_ssid, 5, 1, 1, 1)
        self.spinBox_tcp_port = QtWidgets.QSpinBox(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_tcp_port.sizePolicy().hasHeightForWidth())
        self.spinBox_tcp_port.setSizePolicy(sizePolicy)
        self.spinBox_tcp_port.setMaximumSize(QtCore.QSize(150, 16777215))
        self.spinBox_tcp_port.setWrapping(False)
        self.spinBox_tcp_port.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBox_tcp_port.setAccelerated(True)
        self.spinBox_tcp_port.setMaximum(65535)
        self.spinBox_tcp_port.setProperty("value", 5000)
        self.spinBox_tcp_port.setObjectName("spinBox_tcp_port")
        self.gridLayout_wifi_config.addWidget(self.spinBox_tcp_port, 3, 1, 1, 1)
        self.label_ssid_status_msg = QtWidgets.QLabel(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ssid_status_msg.sizePolicy().hasHeightForWidth())
        self.label_ssid_status_msg.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_ssid_status_msg.setPalette(palette)
        self.label_ssid_status_msg.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_ssid_status_msg.setObjectName("label_ssid_status_msg")
        self.gridLayout_wifi_config.addWidget(self.label_ssid_status_msg, 4, 1, 1, 1)
        self.spinBox_udp_port = QtWidgets.QSpinBox(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_udp_port.sizePolicy().hasHeightForWidth())
        self.spinBox_udp_port.setSizePolicy(sizePolicy)
        self.spinBox_udp_port.setMaximumSize(QtCore.QSize(150, 16777215))
        self.spinBox_udp_port.setSizeIncrement(QtCore.QSize(0, 0))
        self.spinBox_udp_port.setStyleSheet("border: 1px solid red")
        self.spinBox_udp_port.setAccelerated(True)
        self.spinBox_udp_port.setMaximum(65535)
        self.spinBox_udp_port.setProperty("value", 5010)
        self.spinBox_udp_port.setObjectName("spinBox_udp_port")
        self.gridLayout_wifi_config.addWidget(self.spinBox_udp_port, 3, 3, 1, 1)
        self.groupBox_host_ip = QtWidgets.QGroupBox(Form_wifi_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_host_ip.sizePolicy().hasHeightForWidth())
        self.groupBox_host_ip.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.groupBox_host_ip.setPalette(palette)
        self.groupBox_host_ip.setStyleSheet("background:white;\n"
"border: 1px solid rgb(122, 122, 122);")
        self.groupBox_host_ip.setTitle("")
        self.groupBox_host_ip.setFlat(False)
        self.groupBox_host_ip.setObjectName("groupBox_host_ip")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_host_ip)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox_byte_1 = QtWidgets.QSpinBox(self.groupBox_host_ip)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.spinBox_byte_1.setPalette(palette)
        self.spinBox_byte_1.setStyleSheet("border: 0px solid white")
        self.spinBox_byte_1.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_byte_1.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_byte_1.setProperty("showGroupSeparator", False)
        self.spinBox_byte_1.setMaximum(255)
        self.spinBox_byte_1.setObjectName("spinBox_byte_1")
        self.horizontalLayout.addWidget(self.spinBox_byte_1)
        self.label_dot_1 = QtWidgets.QLabel(self.groupBox_host_ip)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dot_1.sizePolicy().hasHeightForWidth())
        self.label_dot_1.setSizePolicy(sizePolicy)
        self.label_dot_1.setStyleSheet("border: 0px solid white")
        self.label_dot_1.setObjectName("label_dot_1")
        self.horizontalLayout.addWidget(self.label_dot_1)
        self.spinBox_byte_2 = QtWidgets.QSpinBox(self.groupBox_host_ip)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.spinBox_byte_2.setPalette(palette)
        self.spinBox_byte_2.setStyleSheet("border: 0px solid white")
        self.spinBox_byte_2.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_byte_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_byte_2.setMaximum(255)
        self.spinBox_byte_2.setObjectName("spinBox_byte_2")
        self.horizontalLayout.addWidget(self.spinBox_byte_2)
        self.label_dot_2 = QtWidgets.QLabel(self.groupBox_host_ip)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dot_2.sizePolicy().hasHeightForWidth())
        self.label_dot_2.setSizePolicy(sizePolicy)
        self.label_dot_2.setStyleSheet("border: 0px solid white")
        self.label_dot_2.setObjectName("label_dot_2")
        self.horizontalLayout.addWidget(self.label_dot_2)
        self.spinBox_byte_3 = QtWidgets.QSpinBox(self.groupBox_host_ip)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.spinBox_byte_3.setPalette(palette)
        self.spinBox_byte_3.setStyleSheet("border: 0px solid white")
        self.spinBox_byte_3.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_byte_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_byte_3.setMaximum(255)
        self.spinBox_byte_3.setObjectName("spinBox_byte_3")
        self.horizontalLayout.addWidget(self.spinBox_byte_3)
        self.label_dot_3 = QtWidgets.QLabel(self.groupBox_host_ip)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dot_3.sizePolicy().hasHeightForWidth())
        self.label_dot_3.setSizePolicy(sizePolicy)
        self.label_dot_3.setStyleSheet("border: 0px solid white")
        self.label_dot_3.setObjectName("label_dot_3")
        self.horizontalLayout.addWidget(self.label_dot_3)
        self.spinBox_byte_4 = QtWidgets.QSpinBox(self.groupBox_host_ip)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.spinBox_byte_4.setPalette(palette)
        self.spinBox_byte_4.setStyleSheet("border: 0px solid white")
        self.spinBox_byte_4.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_byte_4.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_byte_4.setMaximum(255)
        self.spinBox_byte_4.setObjectName("spinBox_byte_4")
        self.horizontalLayout.addWidget(self.spinBox_byte_4)
        self.gridLayout_wifi_config.addWidget(self.groupBox_host_ip, 1, 1, 1, 1)
        self.gridLayout_wifi_config.setColumnStretch(0, 1)
        self.gridLayout_wifi_config.setColumnStretch(1, 4)
        self.gridLayout_wifi_config.setColumnStretch(2, 1)
        self.gridLayout_wifi_config.setColumnStretch(3, 4)
        self.gridLayout_wifi_config.setRowStretch(0, 1)
        self.verticalLayout_wifi_config.addLayout(self.gridLayout_wifi_config)

        self.retranslateUi(Form_wifi_config)
        QtCore.QMetaObject.connectSlotsByName(Form_wifi_config)

    def retranslateUi(self, Form_wifi_config):
        _translate = QtCore.QCoreApplication.translate
        Form_wifi_config.setWindowTitle(_translate("Form_wifi_config", "Form"))
        self.label_udp_port_status_msg.setText(_translate("Form_wifi_config", "This field is required"))
        self.label_host_ip.setText(_translate("Form_wifi_config", "Host IP: "))
        self.label_pass.setText(_translate("Form_wifi_config", "Password: "))
        self.label_ssid.setText(_translate("Form_wifi_config", "SSID:"))
        self.label_tcp_port_status_msg.setText(_translate("Form_wifi_config", "This field is required"))
        self.label_pass_status_msg.setText(_translate("Form_wifi_config", "This field is required"))
        self.label_host_ip_status_msg.setText(_translate("Form_wifi_config", "This field is required"))
        self.label_tcp_port.setText(_translate("Form_wifi_config", "TCP Port:"))
        self.label_udp_port.setText(_translate("Form_wifi_config", "UDP Port:"))
        self.label_ssid_status_msg.setText(_translate("Form_wifi_config", "This field is required"))
        self.label_dot_1.setText(_translate("Form_wifi_config", "."))
        self.label_dot_2.setText(_translate("Form_wifi_config", "."))
        self.label_dot_3.setText(_translate("Form_wifi_config", "."))
