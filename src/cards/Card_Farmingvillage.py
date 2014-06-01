from Card import Card


class Card_Farmingvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 actions, Pull action or treasure from hand"
        self.name = 'Farming Village'
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        """ Reveal cards from the top of your deck until you revel
            an Action or Treasure card. Put that card into your hand
            and discard the other cards. """
        while(1):
            c = player.pickupCard(verbose=False)
            if c.isTreasure() or c.isAction():
                player.output("Added %s to hand" % c.name)
                player.addCard(c, 'hand')
                break
            else:
                player.output("Picked up and discarded %s" % c.name)
                player.discardCard(c)

#EOF
