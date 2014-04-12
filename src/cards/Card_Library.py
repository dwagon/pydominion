from Card import Card

class Card_Library(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'library'
        self.image = 'images/library.jpg'
        self.cost = 5

    def special(self):
        raise NotImplemented

#EOF
