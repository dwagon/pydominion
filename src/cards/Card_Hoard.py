from Card import Card


class Card_Hoard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Gain gold if buy victory"
        self.name = 'Hoard'
        self.gold = 2
        self.cost = 6

    def special(self, game, player):
        """ When this is in play, when you buy a Victory card, gain a Gold """
        print "Not implemented yet"


#EOF
