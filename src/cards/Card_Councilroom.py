from Card import Card

class Card_Councilroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'councilroom'
        self.image = 'images/councilroom.jpg'
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self):
        raise NotImplemented

#EOF
