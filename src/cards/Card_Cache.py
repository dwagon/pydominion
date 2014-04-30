from Card import Card


class Card_Cache(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+3 gold. Gain two coppers"
        self.name = 'Cache'
        self.cost = 5
        self.gold = 3

    def hook_purchasedCard(self, game, player):
        """ When you gain this, gain two Coppers"""
        for i in range(2):
            c = player.gainCard('Copper')
            print "Gained %s" % c.name

#EOF
