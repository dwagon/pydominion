from Card import Card


class Card_Bank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Worth 1 per treasure card in play"
        self.name = 'bank'
        self.image = 'images/bank.jpg'
        self.cost = 7

    def special(self, game, player):
        """ Worth 1 per treasure card in play (counting this)"""
        print "Not implemented yet"

#EOF
