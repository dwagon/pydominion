#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Adventurer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Dig through deck for two treasures"
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


###############################################################################
class Test_Adventurer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['adventurer'])
        self.plr = self.g.playerList(0)

    def test_treasures(self):
        self.plr.setDeck('copper', 'silver', 'gold', 'estate')
        self.plr.setHand('adventurer')
        self.plr.playCard(self.plr.hand[0])
        self.assertEquals(sorted(['Silver', 'Gold']), sorted([c.name for c in self.plr.hand]))
        self.assertEquals(self.plr.discardpile[0].name, 'Estate')
        self.assertEquals(self.plr.deck[0].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
