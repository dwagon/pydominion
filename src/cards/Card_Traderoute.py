from Card import Card


class Card_Traderoute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 buy, +1 gold per token, trash card"
        self.name = 'Trade route'
        self.image = 'images/traderoute.jpg'
        self.cost = 3
        self.buy = 1

    def special(self, game, player):
        """ +1 gold per token on the trade route map. Trash a card
            from your hand. Setup: Put a token on each victory card
            supply pile. When a card is gained from that pile move the
            token to the trade route map """
        print "Not implemented yet"

#EOF
