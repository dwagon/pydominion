from Card import Card


class Card_Goons(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = 'Goons'
        self.cost = 6
        self.buy = 1
        self.gold = 2

    def special(self, game, player):
        """ While this card is in play, when you buy a card +1 VP """
        print "Not implemented yet"


#EOF
