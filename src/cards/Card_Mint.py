from Card import Card


class Card_Mint(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Treasure stuff"
        self.name = 'mint'
        self.image = 'images/mint.jpg'
        self.cost = 5

    def special(self, game, player):
        pass

#EOF
