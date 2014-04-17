from Card import Card


class Card_Forge(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash any number of cards to gain a card"
        self.name = 'forge'
        self.image = 'images/forge.jpg'
        self.cost = 7

    def special(self, game, player):
        """ Trash any number of cards from your hand. Gain a card
            with cost exactly equal to the total cost in coins of the
            trashed cards """
        print "Not implemented yet"

#EOF
