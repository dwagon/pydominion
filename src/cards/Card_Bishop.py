from Card import Card


class Card_Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "bishop stuff"
        self.name = 'bishop'
        self.image = 'images/bishop.jpg'
        self.cost = 1

    def special(self, game, player):
        print "Not implemented yet"

    def special_score(self, game, player):
        print "Not implemented yet"
        return 0

#EOF
