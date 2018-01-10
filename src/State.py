from Card import Card


class State(Card):
    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
        self.cardtype = 'state'
        self.unique_state = False

# EOF
