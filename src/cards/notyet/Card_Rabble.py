from Card import Card


class Card_Rabble(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+3 cards. Other players discard cards"
        self.name = 'Rabble'
        self.cost = 5
        self.cards = 3

    def special(self, game, player):
        """ Each other player reveals the top 3 cards of his deck,
            discard the revealed Actions and Treasures, and puts the
            rest back on top in any order he chooses """
        print "Not implemented yet"

#EOF
