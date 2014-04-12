from Card import Card

class Card_Mine(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'mine'
        self.image = 'images/mine.jpg'
        self.cost = 5

    def special(self):
        raise NotImplemented

#EOF
