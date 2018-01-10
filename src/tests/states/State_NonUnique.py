from State import State


###############################################################################
class State_NonUnique(State):
    def __init__(self):
        State.__init__(self)
        self.desc = "Non Unique State"
        self.name = "NonUnique"

# EOF
