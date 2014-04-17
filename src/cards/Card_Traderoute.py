from Card import Card


class Card_Traderoute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'TODO'
        self.desc = "TODO"
        self.name = 'traderoute'
        self.image = 'images/traderoute.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF
