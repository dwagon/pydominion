from Card import Card


class Card_Expand(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = 'Expand'
        self.cost = 7

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to
            3 more than the trashed card """
        print "Not implemented yet"

#EOF
