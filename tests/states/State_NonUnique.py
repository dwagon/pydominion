from dominion import State, Card


###############################################################################
class State_NonUnique(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.desc = "Non Unique State"
        self.base = Card.CardExpansion.TEST
        self.name = "NonUnique"


# EOF
