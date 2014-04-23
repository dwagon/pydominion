from Card import Card


class Card_Loan(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Play with treasures"
        self.name = 'Loan'
        self.gold = 1
        self.cost = 3

    def special(self, game, player):
        """ When you play this, reveal a card from your deck until
            you reveal a treasure. Discard it or trash it. Discard the
            other cards """
        print "Not implemented yet"

#EOF
