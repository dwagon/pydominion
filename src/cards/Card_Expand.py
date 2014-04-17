from Card import Card


class Card_Expand(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = 'expand'
        self.image = 'images/expand.jpg'
        self.cost = 7

    def special(self, game, player):
        pass

#EOF
