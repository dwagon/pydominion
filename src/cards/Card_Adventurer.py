from Card import Card


class Card_Adventurer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Discard until two treasures"
        self.name = 'Adventurer'
        self.cost = 6

    def special(self, game, player):
        """ Reveal cards from your deck until you reveal two treasure cards
        Add those to your hand and discard the other revealed cards """
        treasures = []
        while len(treasures) < 2:
            c = player.pickupCard(verbose=False)
            if c.isTreasure():
                treasures.append(c)
                player.output("Adding %s" % c.name)
            else:
                player.discardCard(c)

#EOF
