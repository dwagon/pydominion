from Card import Card


class Card_Countinghouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Pull coppers out of discard"
        self.name = 'countinghouse'
        self.image = 'images/countinghouse.jpg'
        self.cost = 5

    def special(self, game, player):
        pass

#EOF
