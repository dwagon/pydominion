from Card import Card


class Card_Grandmarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "+1 card, +1 action, +1 buy, +2 gold"
        self.name = 'Grand Market'
        self.image = 'images/grandmarket.jpg'
        self.cost = 6

    def special(self, game, player):
        """ You can't buy this if you have any copper in play """
        print "Not implemented yet"

#EOF
