# State machine for Telecommand Reception and Routing


from enum import Enum


class ReceiverState(Enum):

    WAITING_FOR_START = 1
    RECEIVING_FRAME = 2
    VALIDATING_FRAME = 3
    EXTRACTING_PACKET = 4
    ROUTING = 5
    DISPATCHING = 6
    COMPLETE = 7
    ERROR = 8


class StateMachine:

    def __init__(self):
        self.state = ReceiverState.WAITING_FOR_START

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state