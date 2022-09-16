from dominion import Card


###############################################################################
class Card_StateTester(Card.Card):
    """Test states"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = "TEST"
        self.desc = "Need a fate/doom card to test states"
        self.name = "StateTester"


# EOF
