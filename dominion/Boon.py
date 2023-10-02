""" https://wiki.dominionstrategy.com/index.php/Boon"""
from dominion import Card


###############################################################################
class BoonPile:
    def __init__(self, cardname, klass):
        self.cardname = cardname
        self.boon = klass()

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.boon, name)

    ###########################################################################
    def __repr__(self):
        return self.name


###############################################################################
class Boon(Card.Card):
    pass


# EOF
