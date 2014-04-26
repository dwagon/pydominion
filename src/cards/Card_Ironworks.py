from Card import Card


class Card_Ironworks(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Gain a card costing up to 4. Extra depending on what it is"
        self.name = 'Iron Works'
        self.cost = 4

    def special(self, player, game):
        """ Gain a card costing up to 4. If it is an action card:
            +1 action; treasure card +1 gold; victory card, +1 card"""
        c = player.plrGainCard(4)
        if c.isVictory():
            player.pickupCard()
            return
        if c.isAction():
            player.t['actions'] += 1
            return
        if c.isTreasure():
            player.t['gold'] += 1
            return
        player.output("What sort of wierd card is %s" % c.name)
#EOF
