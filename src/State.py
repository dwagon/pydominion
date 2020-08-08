from Card import Card


class State(Card):
    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)
        self.cardtype = Card.STATE
        self.unique_state = False

# EOF
