from Card import Card


class Card_Mint(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Treasure stuff"
        self.name = 'Mint'
        self.cost = 5

    def special(self, game, player):
        """ You may reveal a treasure card from your hand. Gain a
            copy of it. When you buy this, trash all treasures you have
            in play"""
        print "Not implemented yet"

#EOF
