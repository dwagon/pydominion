from Card import Card


class Card_Forge(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "TODO"
        self.name = 'forge'
        self.image = 'images/forge.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF
