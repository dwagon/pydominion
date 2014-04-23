from Card import Card


class Card_Contraband(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+3 gold, +1 buy, player to left bans a card purchase"
        self.name = 'Contraband'
        self.cost = 5
        self.gold = 3
        self.buy = 1

    def special(self, game, player):
        """ When you play this, the player to your left names a
            card. You can't buy that card this turn """
        print "Not implemented yet"

#EOF
