from Card import Card


class Card_Quarry(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'TODO'
        self.desc = "TODO"
        self.name = 'quarry'
        self.image = 'images/quarry.jpg'
        self.cost = -1

    def special(self, game, player):
        pass

#EOF
