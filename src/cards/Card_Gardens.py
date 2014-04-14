from Card import Card


class Card_Gardens(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.name = 'gardens'
        self.playable = False
        self.image = 'images/gardens.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

    def special_score(self):
        print "Not implemented"

#EOF
