from Card import Card

class Card_Moat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'moat'
        self.image = 'images/moat.jpg'
        self.defense = True
        self.cost = 2
        self.cards = 2

#EOF
