from Card import Card


class Card_Upgrade(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +1 action. Trash a card and gain one costing 1 more"
        self.name = 'Upgrade'
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to 1 more than it """
        player.output("Trash a card from your hand. Gain a card costing exactly 1 more than it")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = tc.cost
            player.plrGainCard(cost + 1, 'equal')

#EOF
