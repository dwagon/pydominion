from Card import Card


class Card_Venture(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 gold, get next treasure from deck"
        self.name = 'Venture'
        self.image = 'images/venture.jpg'
        self.cost = 5

    def special(self, game, player):
        """ When you play this, reveal cards from your deck until
            you reveal a Treasure. Discard the other cards. Play that
            Treasure """
        print "Not implemented yet"

#EOF
