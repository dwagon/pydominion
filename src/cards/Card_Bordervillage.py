from Card import Card


class Card_Bordervillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 action. When you gain this, gain a card costing less than this"
        self.name = 'Border Village'
        self.cost = 6
        self.cards = 1
        self.actions = 2

    def hook_purchasedCard(self, game, player):
        """ When you gain this, gain a card costing less than this"""
        newcost = self.cost - 1
        player.output("Gain a card costing %d due to Border Village" % newcost)
        player.plrGainCard(cost=newcost)

#EOF
