from Card import Card


class Card_Bank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Worth 1 per treasure card in play"
        self.name = 'Bank'
        self.cost = 7

    def special(self, game, player):
        """ Worth 1 per treasure card in play (counting this)"""
        g = 1   # Counting this
        for c in player.hand:
            if c.isTreasure():
                g += 1
        print("Gained %d gold from bank" % g)
        player.t['gold'] += g

#EOF
