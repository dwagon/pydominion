#!/usr/bin/env python

import unittest
import Card
import Game
from Hex import Hex


###############################################################################
class Hex_Poverty(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = Card.HEX
        self.base = Game.NOCTURNE
        self.desc = "Discard down to 3 cards in hand"
        self.name = "Poverty"
        self.purchasable = False

    def special(self, game, player):
        player.plrDiscardDownTo(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Poverty(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Poverty":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_normal(self):
        self.plr.test_input = ['1', '2', '0']
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
