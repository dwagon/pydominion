#!/usr/bin/env python

import unittest
from dominion import Card, Game, Hex


###############################################################################
class Hex_Greed(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = "Gain a Copper onto your deck."
        self.name = "Greed"
        self.purchasable = False

    def special(self, game, player):
        player.gainCard("Copper", "deck")


###############################################################################
class Test_Greed(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Greed":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_famine(self):
        self.plr.set_deck("Duchy", "Cursed Village", "Gold")
        self.plr.gainCard("Cursed Village")
        self.assertIsNotNone(self.plr.in_discard("Cursed Village"))
        self.assertIsNotNone(self.plr.in_deck("Copper"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
