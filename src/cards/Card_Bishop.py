from Card import Card


class Card_Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card for VP"
        self.name = 'Bishop'
        self.gold = 1
        self.victory = 1
        self.cost = 4

    def special(self, game, player):
        """ Trash a card from your hand. +VP equal to half its cost
        in coins, rounded down. Each other player may trash a card
        from his hand """
        print "Not implemented yet"


#EOF
