from Card import Card


class Card_Peddler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +1 action, +1 gold"
        self.name = 'Pedler'
        self.card = 1
        self.action = 1
        self.gold = 1
        self.cost = 8   # TODO - special

    def special(self, game, player):
        """ During your buy pahse this costs 2 less per action card
            you have in play, but not less than 0 """
        print "Not implemented yet"

#EOF
