from Card import Card


class Card_Watchtower(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "TODO"
        self.name = 'watchtower'
        self.image = 'images/watchtower.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF
