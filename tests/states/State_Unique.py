from dominion import State


###############################################################################
class State_Lost_in_woods(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.desc = "Unique Test State"
        self.base = "TEST"
        self.name = "Unique"
        self.unique_state = True


# EOF
