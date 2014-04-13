from Card import Card

class Card_Bureaucrat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'bureaucrat'
        self.image = 'images/bureaucrat.jpg'
        self.cost = 4

    def special(self, game, player):
        print "Not Implemented"

#EOF
