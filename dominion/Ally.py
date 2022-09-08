from dominion import Card


###############################################################################
class Ally(Card.Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cardtype = Card.TYPE_ALLY


###############################################################################
class AllyPile:
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.ally = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.ally, name)

    ###########################################################################
    def __repr__(self):
        return self.name


# EOF
