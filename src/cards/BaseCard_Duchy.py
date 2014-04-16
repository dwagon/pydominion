from Card import Card


class Card_Duchy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "3 VP"
        self.playable = False
        self.name = 'duchy'
        self.image = 'images/duchy.jpg'
        self.cost = 5
        self.victory = 3

#EOF
