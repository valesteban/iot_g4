from PyQt5.QtWidgets import QWidget, QLayout

from PyQt5.QtCore import QAbstractTransition, QState, QSignalTransition
from PyQt5.QtCore import pyqtBoundSignal
import typing

from gui.all_events import *
#from gui.esp_dev import ESPConfig
#from gui.esp_lists import ESPDicts, ListsMachine
#from gui.live_plot import PlotListsMachine

class EndFindTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != EndFindEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPFoundTransition(QAbstractTransition):
    def __init__(self, esp_list: "ESPDicts", sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.found_event = None
        self.esp_list = esp_list

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPFoundEvent.EVENT_TYPE:
        
            return False
        else:
            self.found_event = event
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 

    def transition_slot(self):
        print("hellow")
        print(self.found_event.esp_id, self.found_event.esp_mac)
        self.esp_list.check_esp(self.found_event.esp_id, self.found_event.esp_mac)


class ESPAddFoundTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddFoundEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_found += 1
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPRemoveFoundTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPRemoveFoundEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_found -= 1
            
            self.list_layout.removeWidget(event.esp_widget)
            event.esp_widget.setParent(None)
            if self.esp_lists.num_found == 0:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPActiveTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPActiveEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 
            

class ESPAddActiveTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPAddActiveEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_active += 1
            event.esp_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.esp_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class ESPRemoveActiveTransition(QAbstractTransition):
    def __init__(self, esp_lists: "ListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.esp_lists = esp_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPRemoveActiveEvent.EVENT_TYPE:
            return False
        else:
            self.esp_lists.num_active -= 1
            self.list_layout.removeWidget(event.esp_widget)
            event.esp_widget.setParent(None)
            
            if self.esp_lists.num_active == 0:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return 


class CheckNoWifiTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != CheckNoWifiEvent.EVENT_TYPE:
            return False
        else:
            if not event.config_wifi and not event.send_wifi:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return 

class UnableToSendTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != UnableToSendEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class AbleToSendTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != AbleToSendEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class InvalidWifiConfigTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != InvalidWifiConfigEvent.EVENT_TYPE:
            return False
        else:
            if event.should_transition:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return

class ValidWifiConfigTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ValidWifiConfigEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class SendStartTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != SendStartEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class InactiveESPTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != InactiveESPEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class LivePlotAddTransition(QAbstractTransition):
    def __init__(self, plot_lists: "PlotListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.plot_lists = plot_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotAddEvent.EVENT_TYPE:
            return False
        else:
            self.plot_lists.num_plots += 1
            event.plot_widget.setParent(self.widget_list_parent)
            self.list_layout.addWidget(event.plot_widget)
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return 


class LivePlotRemoveTransition(QAbstractTransition):
    def __init__(self, plot_lists: "PlotListsMachine", widget_list_parent: QWidget, list_layout: QLayout, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)
        self.plot_lists = plot_lists
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotRemoveEvent.EVENT_TYPE:
            return False
        else:
            self.plot_lists.num_plots -= 1
            
            self.list_layout.removeWidget(event.plot_widget)
            event.plot_widget.setParent(None)
            if self.plot_lists.num_plots == 0:
                return True
            return False

    def onTransition(self, event: 'QEvent') -> None:
        return 

class ESPConfiguringTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPConfiguringEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class ESPSendingTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPSendingEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class ESPSleepingTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPSleepingEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class ESPErroringTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != ESPErroringEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return


class StartClickTransition(QSignalTransition):
    def __init__(self, esp_config: "ESPConfig", signal: pyqtBoundSignal, sourceState: typing.Optional['QState'] = None) -> None: 
        super().__init__(signal, sourceState)
        self.esp_config = esp_config

    def eventTest(self, event: 'QEvent') -> bool:
        if not super().eventTest(event):
            return False
        else:
            result = self.esp_config.wifi_properties.validate_all(*self.esp_config.wifi_ui.get_all_ui_values())
            self.esp_config.machine.postEvent(InvalidWifiConfigEvent(not result))
            if hasattr(self.sourceState(), "should_send") and self.sourceState().should_send(result):
                self.esp_config.esp.machine.postEvent(SendStartEvent())
                return True
            else:
                return False

class LivePlotNoIDTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotNoIDEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class LivePlotReadyTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotReadyEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return

class LivePlotPlottingTransition(QAbstractTransition):
    def __init__(self, sourceState: typing.Optional['QState'] = None) -> None:
        super().__init__(sourceState)

    def eventTest(self, event: 'QEvent') -> bool:
        if event.type() != LivePlotPlottingEvent.EVENT_TYPE:
            return False
        else:
            return True

    def onTransition(self, event: 'QEvent') -> None:
        return