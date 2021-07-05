import Card


###############################################################################
class Card_StateTester(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = "TEST"
        self.desc = "Need a fate/doom card to test states"
        self.name = "StateTester"


# EOF
