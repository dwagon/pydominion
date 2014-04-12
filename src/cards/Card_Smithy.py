from Card import Card

class Card_Smithy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'smith'
        self.image = 'images/smith.jpg'
        self.cards = 3
        self.cost = 4

#EOF
