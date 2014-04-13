from Card import Card

class Card_Chancellor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'chancellor'
        self.image = 'images/chancellor.jpg'
        self.gold = 2
        self.cost = 3

    def special(self, game, player):
        print "Not Implemented"

#EOF
