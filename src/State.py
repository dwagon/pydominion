import Card


class State(Card.Card):
    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)
        self.cardtype = Card.TYPE_STATE
        self.unique_state = False


# EOF
