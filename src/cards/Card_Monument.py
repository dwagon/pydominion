from Card import Card


class Card_Monument(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold, +1 VP"
        self.name = 'monument'
        self.image = 'images/monument.jpg'
        self.cost = 4
        self.gold = 2
        self.score = 1

    def special(self, game, player):
        pass

#EOF
