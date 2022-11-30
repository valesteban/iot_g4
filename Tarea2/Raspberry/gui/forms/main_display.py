# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Users\valeg\Documents\IoT\iot_g4\Tarea2\Raspberry\extra\qt\main_display.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(796, 682)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_central_widget = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_central_widget.setObjectName("verticalLayout_central_widget")
        self.tabWidget_menus = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_menus.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_menus.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_menus.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget_menus.setUsesScrollButtons(True)
        self.tabWidget_menus.setDocumentMode(False)
        self.tabWidget_menus.setTabsClosable(False)
        self.tabWidget_menus.setMovable(False)
        self.tabWidget_menus.setTabBarAutoHide(False)
        self.tabWidget_menus.setObjectName("tabWidget_menus")
        self.tab_menu_esp = QtWidgets.QWidget()
        self.tab_menu_esp.setObjectName("tab_menu_esp")
        self.verticalLayout_menu_esp = QtWidgets.QVBoxLayout(self.tab_menu_esp)
        self.verticalLayout_menu_esp.setObjectName("verticalLayout_menu_esp")
        self.stackedWidget_rasp_status = QtWidgets.QStackedWidget(self.tab_menu_esp)
        self.stackedWidget_rasp_status.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget_rasp_status.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stackedWidget_rasp_status.setObjectName("stackedWidget_rasp_status")
        self.page_main_esp = QtWidgets.QWidget()
        self.page_main_esp.setObjectName("page_main_esp")
        self.verticalLayout_main_esp = QtWidgets.QVBoxLayout(self.page_main_esp)
        self.verticalLayout_main_esp.setObjectName("verticalLayout_main_esp")
        self.frame_search = QtWidgets.QFrame(self.page_main_esp)
        self.frame_search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_search.setObjectName("frame_search")
        self.verticalLayout_search = QtWidgets.QVBoxLayout(self.frame_search)
        self.verticalLayout_search.setObjectName("verticalLayout_search")
        self.horizontalLayout_search_heading = QtWidgets.QHBoxLayout()
        self.horizontalLayout_search_heading.setObjectName("horizontalLayout_search_heading")
        self.label_icon_search = QtWidgets.QLabel(self.frame_search)
        self.label_icon_search.setMaximumSize(QtCore.QSize(30, 30))
        self.label_icon_search.setText("")
        self.label_icon_search.setPixmap(QtGui.QPixmap(":/icon_esp/images/esp.jpg"))
        self.label_icon_search.setScaledContents(True)
        self.label_icon_search.setObjectName("label_icon_search")
        self.horizontalLayout_search_heading.addWidget(self.label_icon_search)
        self.label_search_title = QtWidgets.QLabel(self.frame_search)
        self.label_search_title.setObjectName("label_search_title")
        self.horizontalLayout_search_heading.addWidget(self.label_search_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_search_heading.addItem(spacerItem)
        self.verticalLayout_search.addLayout(self.horizontalLayout_search_heading)
        self.scrollArea_found_area = QtWidgets.QScrollArea(self.frame_search)
        self.scrollArea_found_area.setWidgetResizable(True)
        self.scrollArea_found_area.setObjectName("scrollArea_found_area")
        self.scrollAreaWidgetContents_found_area = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_found_area.setGeometry(QtCore.QRect(0, 0, 698, 85))
        self.scrollAreaWidgetContents_found_area.setObjectName("scrollAreaWidgetContents_found_area")
        self.verticalLayout_found_area = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_found_area)
        self.verticalLayout_found_area.setObjectName("verticalLayout_found_area")
        self.verticalLayout_found_list = QtWidgets.QVBoxLayout()
        self.verticalLayout_found_list.setObjectName("verticalLayout_found_list")
        self.verticalLayout_found_area.addLayout(self.verticalLayout_found_list)
        self.scrollArea_found_area.setWidget(self.scrollAreaWidgetContents_found_area)
        self.verticalLayout_search.addWidget(self.scrollArea_found_area)
        self.horizontalLayout_search_bottom = QtWidgets.QHBoxLayout()
        self.horizontalLayout_search_bottom.setObjectName("horizontalLayout_search_bottom")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_search_bottom.addItem(spacerItem1)
        self.pushButton_search_refresh = QtWidgets.QPushButton(self.frame_search)
        self.pushButton_search_refresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_refresh/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_search_refresh.setIcon(icon)
        self.pushButton_search_refresh.setObjectName("pushButton_search_refresh")
        self.horizontalLayout_search_bottom.addWidget(self.pushButton_search_refresh)
        self.verticalLayout_search.addLayout(self.horizontalLayout_search_bottom)
        self.verticalLayout_main_esp.addWidget(self.frame_search)
        self.frame_active = QtWidgets.QFrame(self.page_main_esp)
        self.frame_active.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_active.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_active.setObjectName("frame_active")
        self.verticalLayout_active = QtWidgets.QVBoxLayout(self.frame_active)
        self.verticalLayout_active.setObjectName("verticalLayout_active")
        self.label_active = QtWidgets.QLabel(self.frame_active)
        self.label_active.setObjectName("label_active")
        self.verticalLayout_active.addWidget(self.label_active)
        self.scrollArea_active = QtWidgets.QScrollArea(self.frame_active)
        self.scrollArea_active.setWidgetResizable(True)
        self.scrollArea_active.setObjectName("scrollArea_active")
        self.scrollAreaWidgetContents_active_esp = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_active_esp.setGeometry(QtCore.QRect(0, 0, 698, 343))
        self.scrollAreaWidgetContents_active_esp.setObjectName("scrollAreaWidgetContents_active_esp")
        self.verticalLayout_active_esp = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_active_esp)
        self.verticalLayout_active_esp.setObjectName("verticalLayout_active_esp")
        self.verticalLayout_active_list = QtWidgets.QVBoxLayout()
        self.verticalLayout_active_list.setObjectName("verticalLayout_active_list")
        self.verticalLayout_active_esp.addLayout(self.verticalLayout_active_list)
        self.scrollArea_active.setWidget(self.scrollAreaWidgetContents_active_esp)
        self.verticalLayout_active.addWidget(self.scrollArea_active)
        self.verticalLayout_main_esp.addWidget(self.frame_active)
        self.verticalLayout_main_esp.setStretch(0, 3)
        self.verticalLayout_main_esp.setStretch(1, 7)
        self.stackedWidget_rasp_status.addWidget(self.page_main_esp)
        self.page_no_rasp = QtWidgets.QWidget()
        self.page_no_rasp.setObjectName("page_no_rasp")
        self.verticalLayout_no_rasp = QtWidgets.QVBoxLayout(self.page_no_rasp)
        self.verticalLayout_no_rasp.setObjectName("verticalLayout_no_rasp")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_no_rasp.addItem(spacerItem2)
        self.horizontalLayout_icon_no_rasp = QtWidgets.QHBoxLayout()
        self.horizontalLayout_icon_no_rasp.setObjectName("horizontalLayout_icon_no_rasp")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_icon_no_rasp.addItem(spacerItem3)
        self.label_icon_no_rasp = QtWidgets.QLabel(self.page_no_rasp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon_no_rasp.sizePolicy().hasHeightForWidth())
        self.label_icon_no_rasp.setSizePolicy(sizePolicy)
        self.label_icon_no_rasp.setMaximumSize(QtCore.QSize(200, 200))
        self.label_icon_no_rasp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_icon_no_rasp.setText("")
        self.label_icon_no_rasp.setPixmap(QtGui.QPixmap(":/icon_disconnected/images/plug.png"))
        self.label_icon_no_rasp.setScaledContents(True)
        self.label_icon_no_rasp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_icon_no_rasp.setWordWrap(False)
        self.label_icon_no_rasp.setIndent(0)
        self.label_icon_no_rasp.setObjectName("label_icon_no_rasp")
        self.horizontalLayout_icon_no_rasp.addWidget(self.label_icon_no_rasp)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_icon_no_rasp.addItem(spacerItem4)
        self.verticalLayout_no_rasp.addLayout(self.horizontalLayout_icon_no_rasp)
        self.label_no_rasp_message = QtWidgets.QLabel(self.page_no_rasp)
        self.label_no_rasp_message.setLocale(QtCore.QLocale(QtCore.QLocale.Spanish, QtCore.QLocale.Chile))
        self.label_no_rasp_message.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_no_rasp_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_no_rasp_message.setObjectName("label_no_rasp_message")
        self.verticalLayout_no_rasp.addWidget(self.label_no_rasp_message)
        self.horizontalLayout_no_rasp_reconnect = QtWidgets.QHBoxLayout()
        self.horizontalLayout_no_rasp_reconnect.setObjectName("horizontalLayout_no_rasp_reconnect")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_no_rasp_reconnect.addItem(spacerItem5)
        self.pushButton_no_rasp_reconnect = QtWidgets.QPushButton(self.page_no_rasp)
        self.pushButton_no_rasp_reconnect.setObjectName("pushButton_no_rasp_reconnect")
        self.horizontalLayout_no_rasp_reconnect.addWidget(self.pushButton_no_rasp_reconnect)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_no_rasp_reconnect.addItem(spacerItem6)
        self.verticalLayout_no_rasp.addLayout(self.horizontalLayout_no_rasp_reconnect)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_no_rasp.addItem(spacerItem7)
        self.stackedWidget_rasp_status.addWidget(self.page_no_rasp)
        self.verticalLayout_menu_esp.addWidget(self.stackedWidget_rasp_status)
        self.tabWidget_menus.addTab(self.tab_menu_esp, "")
        self.tab_menu_plots = QtWidgets.QWidget()
        self.tab_menu_plots.setObjectName("tab_menu_plots")
        self.verticalLayout_menu_plots = QtWidgets.QVBoxLayout(self.tab_menu_plots)
        self.verticalLayout_menu_plots.setObjectName("verticalLayout_menu_plots")
        self.horizontalLayout_add_live_plot = QtWidgets.QHBoxLayout()
        self.horizontalLayout_add_live_plot.setObjectName("horizontalLayout_add_live_plot")
        self.pushButton_add_live_plot = QtWidgets.QPushButton(self.tab_menu_plots)
        self.pushButton_add_live_plot.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon_add/images/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add_live_plot.setIcon(icon1)
        self.pushButton_add_live_plot.setObjectName("pushButton_add_live_plot")
        self.horizontalLayout_add_live_plot.addWidget(self.pushButton_add_live_plot)
        self.label_add_live_plot = QtWidgets.QLabel(self.tab_menu_plots)
        self.label_add_live_plot.setLocale(QtCore.QLocale(QtCore.QLocale.Spanish, QtCore.QLocale.Chile))
        self.label_add_live_plot.setObjectName("label_add_live_plot")
        self.horizontalLayout_add_live_plot.addWidget(self.label_add_live_plot)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_add_live_plot.addItem(spacerItem8)
        self.verticalLayout_menu_plots.addLayout(self.horizontalLayout_add_live_plot)
        self.stackedWidget_plot_count = QtWidgets.QStackedWidget(self.tab_menu_plots)
        self.stackedWidget_plot_count.setObjectName("stackedWidget_plot_count")
        self.page_added_plots = QtWidgets.QWidget()
        self.page_added_plots.setObjectName("page_added_plots")
        self.verticalLayout_added_plots = QtWidgets.QVBoxLayout(self.page_added_plots)
        self.verticalLayout_added_plots.setObjectName("verticalLayout_added_plots")
        self.scrollArea_added_plots = QtWidgets.QScrollArea(self.page_added_plots)
        self.scrollArea_added_plots.setWidgetResizable(True)
        self.scrollArea_added_plots.setObjectName("scrollArea_added_plots")
        self.scrollAreaWidgetContents_added_plots = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_added_plots.setGeometry(QtCore.QRect(0, 0, 722, 547))
        self.scrollAreaWidgetContents_added_plots.setObjectName("scrollAreaWidgetContents_added_plots")
        self.verticalLayout_scroll_added_plots = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_added_plots)
        self.verticalLayout_scroll_added_plots.setObjectName("verticalLayout_scroll_added_plots")
        self.verticalLayout_added_plots_list = QtWidgets.QVBoxLayout()
        self.verticalLayout_added_plots_list.setObjectName("verticalLayout_added_plots_list")
        self.verticalLayout_scroll_added_plots.addLayout(self.verticalLayout_added_plots_list)
        self.scrollArea_added_plots.setWidget(self.scrollAreaWidgetContents_added_plots)
        self.verticalLayout_added_plots.addWidget(self.scrollArea_added_plots)
        self.stackedWidget_plot_count.addWidget(self.page_added_plots)
        self.page_no_plot = QtWidgets.QWidget()
        self.page_no_plot.setObjectName("page_no_plot")
        self.verticalLayout_no_plot = QtWidgets.QVBoxLayout(self.page_no_plot)
        self.verticalLayout_no_plot.setObjectName("verticalLayout_no_plot")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_no_plot.addItem(spacerItem9)
        self.horizontalLayout_no_plot_icon = QtWidgets.QHBoxLayout()
        self.horizontalLayout_no_plot_icon.setObjectName("horizontalLayout_no_plot_icon")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_no_plot_icon.addItem(spacerItem10)
        self.label_no_plot_icon = QtWidgets.QLabel(self.page_no_plot)
        self.label_no_plot_icon.setMaximumSize(QtCore.QSize(180, 200))
        self.label_no_plot_icon.setText("")
        self.label_no_plot_icon.setPixmap(QtGui.QPixmap(":/icon_plot/images/scatter-graph.png"))
        self.label_no_plot_icon.setScaledContents(True)
        self.label_no_plot_icon.setObjectName("label_no_plot_icon")
        self.horizontalLayout_no_plot_icon.addWidget(self.label_no_plot_icon)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_no_plot_icon.addItem(spacerItem11)
        self.verticalLayout_no_plot.addLayout(self.horizontalLayout_no_plot_icon)
        self.label_no_plot = QtWidgets.QLabel(self.page_no_plot)
        self.label_no_plot.setLocale(QtCore.QLocale(QtCore.QLocale.Spanish, QtCore.QLocale.Chile))
        self.label_no_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_no_plot.setObjectName("label_no_plot")
        self.verticalLayout_no_plot.addWidget(self.label_no_plot)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_no_plot.addItem(spacerItem12)
        self.stackedWidget_plot_count.addWidget(self.page_no_plot)
        self.verticalLayout_menu_plots.addWidget(self.stackedWidget_plot_count)
        self.tabWidget_menus.addTab(self.tab_menu_plots, "")
        self.tab_menu_bd = QtWidgets.QWidget()
        self.tab_menu_bd.setObjectName("tab_menu_bd")
        self.tabWidget_menus.addTab(self.tab_menu_bd, "")
        self.verticalLayout_central_widget.addWidget(self.tabWidget_menus)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget_menus.setCurrentIndex(0)
        self.stackedWidget_rasp_status.setCurrentIndex(0)
        self.stackedWidget_plot_count.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_search_title.setText(_translate("MainWindow", "Searching for devices"))
        self.label_active.setText(_translate("MainWindow", "Active devices"))
        self.label_no_rasp_message.setText(_translate("MainWindow", "The connection with the Raspberry has been lost"))
        self.pushButton_no_rasp_reconnect.setText(_translate("MainWindow", "Reconnect"))
        self.tabWidget_menus.setTabText(self.tabWidget_menus.indexOf(self.tab_menu_esp), _translate("MainWindow", "ESP Connection"))
        self.label_add_live_plot.setText(_translate("MainWindow", "Add Live Plot"))
        self.label_no_plot.setText(_translate("MainWindow", "Add a Live Plot to visualize data directly from data base"))
        self.tabWidget_menus.setTabText(self.tabWidget_menus.indexOf(self.tab_menu_plots), _translate("MainWindow", "Live Plot"))
        self.tabWidget_menus.setTabText(self.tabWidget_menus.indexOf(self.tab_menu_bd), _translate("MainWindow", "Database"))
from . import icons_rc