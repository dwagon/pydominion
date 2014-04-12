from Card import Card

class Card_Feast(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'feast'
        self.image = 'images/feast.jpg'
        self.cost = 4

    def special(self):
        raise NotImplemented

#EOF
