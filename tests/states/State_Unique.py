from dominion import State, Card


###############################################################################
class State_Unique(State.State):
    """Test State"""

    def __init__(self):
        State.State.__init__(self)
        self.desc = "Unique Test State"
        self.base = Card.CardExpansion.TEST
        self.name = "Unique"
        self.unique_state = True


# EOF
