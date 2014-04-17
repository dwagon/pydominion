from Card import Card


class Card_Colony(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "+10 VP"
        self.name = 'colony'
        self.playable = False
        self.image = 'images/colony.jpg'
        self.cost = 11


#EOF
