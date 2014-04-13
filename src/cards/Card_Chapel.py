from Card import Card

class Card_Chapel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'chapel'
        self.image = 'images/chapel.jpg'
        self.cost = 2

    def special(self, game, player):
        print "Not Implemented"

#EOF
