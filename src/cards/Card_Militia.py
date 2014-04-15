from Card import Card


class Card_Militia(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'attack'
        self.name = 'militia'
        self.image = 'images/militia.jpg'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        print "Not Implemented"

#EOF
