#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Greed(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocturne'
        self.desc = "Gain a Copper onto your deck."
        self.name = "Greed"
        self.purchasable = False

    def special(self, game, player):
        player.gainCard('Copper', 'deck')


###############################################################################
class Test_Greed(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "Greed":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self):
        self.plr.setDeck('Duchy', 'Cursed Village', 'Gold')
        self.plr.gainCard('Cursed Village')
        self.assertIsNotNone(self.plr.inDiscard('Cursed Village'))
        self.assertIsNotNone(self.plr.inDeck('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
