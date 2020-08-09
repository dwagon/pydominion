import Card


class Project(Card.Card):
    def __init__(self, *args, **kwargs):
        Card.Card.__init__(self, *args, **kwargs)
        self.cardtype = Card.PROJECT

# EOF
