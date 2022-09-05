""" Test Card for Old Cards """
from dominion import Card


###############################################################################
class Card_OldCard(Card.Card):
    """ Test card for old cards """
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = "TEST"
        self.desc = "Test old cards"
        self.name = "OldCard"


# EOF
