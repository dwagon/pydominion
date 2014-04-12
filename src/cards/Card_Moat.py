from Card import Card

class Card_Moat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'moat'
        self.image = 'images/moat.jpg'
        self.cost = 2

    def special(self):
        raise NotImplemented

#EOF
