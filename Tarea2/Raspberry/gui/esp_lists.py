from PyQt5.QtWidgets import QWidget, QLayout
from PyQt5.QtCore import QStateMachine, QState


from gui.transitions import ESPAddFoundTransition, ESPAddActiveTransition, ESPRemoveActiveTransition, ESPRemoveFoundTransition
from gui.all_events import ESPFoundEvent
#from gui.esp_dev import ESPDevice

class ListsMachine:
    def __init__(self, widget_list_parent: QWidget, list_layout: QLayout, widget_active_list_parent: QWidget, list_active_layout: QLayout) -> None:
        self.num_found  = 0
        self.num_active = 0
        self.widget_list_parent= widget_list_parent
        self.list_layout = list_layout
        self.widget_active_list_parent = widget_active_list_parent
        self.active_list_layout = list_active_layout

        self.machine = QStateMachine()
        state_parallel = QState(childMode=QState.ChildMode.ParallelStates, parent=self.machine)

        state_emptiness = QState(state_parallel)
        state_adding = QState(state_parallel)

        state_found_empty = QState(state_emptiness)
        state_found_filled = QState(state_emptiness)
        state_active_empty = QState(state_adding)
        state_active_filled = QState(state_adding)

        # transitions

        trans_found_empty_to_filled = ESPAddFoundTransition(self, self.widget_list_parent, self.list_layout)
        trans_found_empty_to_filled.setTargetState(state_found_filled)
        state_found_empty.addTransition(trans_found_empty_to_filled)

        trans_found_to_found = ESPAddFoundTransition(self, self.widget_list_parent, self.list_layout)
        state_found_filled.addTransition(trans_found_to_found)

        trans_active_empty_to_filled = ESPAddActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        trans_active_empty_to_filled.setTargetState(state_active_filled)
        state_active_empty.addTransition(trans_active_empty_to_filled)

        trans_active_to_active = ESPAddActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        state_active_filled.addTransition(trans_active_to_active)

        trans_found_filled_to_empty = ESPRemoveFoundTransition(self, self.widget_list_parent, self.list_layout)
        trans_found_filled_to_empty.setTargetState(state_found_empty)
        state_found_filled.addTransition(trans_found_filled_to_empty)

        trans_active_filled_to_empty = ESPRemoveActiveTransition(self, self.widget_active_list_parent,self.active_list_layout)
        trans_active_filled_to_empty.setTargetState(state_active_empty)
        state_active_filled.addTransition(trans_active_filled_to_empty)

        state_emptiness.setInitialState(state_found_empty)
        state_adding.setInitialState(state_active_empty)

        self.machine.setInitialState(state_parallel)
        self.machine.start()

