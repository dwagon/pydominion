from Card import Card


###############################################################################
class Card_StateTester(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.desc = "Need a fate/doom card to test states"
        self.name = 'StateTester'

# EOF
