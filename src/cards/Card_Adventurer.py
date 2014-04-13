from Card import Card

class Card_Adventurer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'adventurer'
        self.image = 'images/adventurer.jpg'
        self.cost = 6

    def special(self, game, player):
        print "Not Implemented"

#EOF
