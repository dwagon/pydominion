from State import State


###############################################################################
class State_Lost_in_woods(State):
    def __init__(self):
        State.__init__(self)
        self.desc = "Unique Test State"
        self.base = "TEST"
        self.name = "Unique"
        self.unique_state = True


# EOF
