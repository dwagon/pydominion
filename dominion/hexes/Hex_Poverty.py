#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_Poverty(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = "Discard down to 3 cards in hand"
        self.name = "Poverty"
        self.purchasable = False

    def special(self, game, player):
        player.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Poverty(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Poverty":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_normal(self):
        self.plr.test_input = ["1", "2", "0"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
