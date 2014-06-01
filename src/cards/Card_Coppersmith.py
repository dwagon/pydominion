from Card import Card


class Card_Coppersmith(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Copper produces and extra +1 this turn"
        self.name = 'Coppersmith'
        self.cost = 4

    def hook_spendValue(self, game, player, card):
        """ Copper produces an extra 1 this turn """
        if card.name == 'Copper':
            print "Copper worth 1 more"
            return 1
        return 0

#EOF
