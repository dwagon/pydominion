#!/usr/bin/env python

import unittest
import Game
from Hex import Hex


###############################################################################
class Hex_Delusion(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = Game.NOCTURNE
        self.desc = "If you don't have Deluded or Envious, take Deluded."
        self.name = "Delusion"
        self.purchasable = False

    def special(self, game, player):
        if player.has_state('Deluded') or player.has_state('Envious'):
            return
        player.assign_state('Deluded')


###############################################################################
class Test_Delusion(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_preexisting(self):
        self.plr.assign_state('Envious')
        self.plr.gainCard('Cursed Village')
        self.assertTrue(self.plr.has_state('Envious'))

    def test_normal(self):
        self.plr.gainCard('Cursed Village')
        self.assertTrue(self.plr.has_state('Deluded'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
