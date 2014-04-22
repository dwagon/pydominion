from Card import Card


class Card_Shantytown(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "If no action in hand, +2 cards"
        self.name = 'Shanty Town'
        self.actions = 2
        self.cost = 3

    def special(self, game, player):
        """ Reveal your hand. If you have no Action cards in hand, +2 cards"""
        for c in player.hand:
            if c.isAction():
                break
        else:
            for i in range(2):
                c = player.pickupCard()
                print "Picked up %s" % c.name

#EOF
