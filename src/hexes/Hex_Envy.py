#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Envy(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocture'
        self.desc = "If you don't have Deluded or Envious, take Envious."
        self.name = "Envy"
        self.purchasable = False

    def special(self, game, player):
        if player.has_state('Deluded') or player.has_state('Envious'):
            return
        player.assign_state('Envious')


###############################################################################
class Test_Envy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "Envy":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_preexisting(self):
        self.plr.assign_state('Deluded')
        self.plr.gainCard('Cursed Village')
        self.assertTrue(self.plr.has_state('Deluded'))

    def test_normal(self):
        self.plr.gainCard('Cursed Village')
        self.assertTrue(self.plr.has_state('Envious'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
