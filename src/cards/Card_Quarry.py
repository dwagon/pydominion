from Card import Card


class Card_Quarry(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 gold, action cards cost 2 less"
        self.name = 'Quarry'
        self.image = 'images/quarry.jpg'
        self.cost = 4
        self.gold = 1

    def special(self, game, player):
        """ While this is in play, action cards cost 2 less, but
            not less than 0"""
        print "Not implemented yet"

#EOF
