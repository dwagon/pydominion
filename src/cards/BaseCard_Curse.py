from Card import Card

class Card_Curse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.playable = False
        self.name = 'curse'
        self.image = 'images/curse.jpg'
        self.cost = 0
        self.victory = -1

#EOF
