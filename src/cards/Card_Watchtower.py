from Card import Card


class Card_Watchtower(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Draw up to 6 cards. Can trash gained cards or put on top of deck"
        self.name = 'Watchtower'
        self.cost = 3

    def special(self, game, player):
        """ Draw until you have 6 cards in hand. When you gain a
            card, you may reveal this from your hand. If you do, either
            trash that card, or put it on top of your deck """
        print "Not implemented yet"

#EOF
