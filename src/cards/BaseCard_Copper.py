from Card import Card

class Card_Copper(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.selectable = False
        self.name = 'copper'
        self.image = 'images/copper.jpg'
        self.gold = 1
        self.cost = 0

#EOF
