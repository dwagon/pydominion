from Card import Card


class Card_Remodel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a card and gain one costing 2 more"
        self.name = 'Remodel'
        self.cost = 2

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to
            2 more than the trashed card """
        print("Trash a card from your hand. Gain another costing up to 2 more than the one you trashed")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = tc.cost
            player.plrGainCard(cost + 2)

#EOF
