from Card import Card


class Card_Talisman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 gold. Gain copy of non-victory cards you buy"
        self.name = 'talisman'
        self.image = 'images/talisman.jpg'
        self.cost = 4
        self.gold = 1

    def special(self, game, player):
        """ While this is in play, when you buy a card costing 4
            or less that is not a victory card, gain a copy of it."""
        print "Not implemented yet"

#EOF
