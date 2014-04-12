from Card import Card

class Card_Cellar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'cellar'
        self.image = 'images/cellar.jpg'
        self.action = 1
        self.cost = 2

    def special(self):
        raise NotImplemented

#EOF
