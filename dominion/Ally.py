""" https://wiki.dominionstrategy.com/index.php/Ally"""
from dominion import Card


###############################################################################
class Ally(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ALLY


# EOF
