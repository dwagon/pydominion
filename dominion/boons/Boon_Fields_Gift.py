#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game


###############################################################################
class Boon_Fields_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Action; +1 Coin"
        self.name = "The Field's Gift"
        self.purchasable = False
        self.coin = 1
        self.actions = 1
        self.retain_boon = True


###############################################################################
class Test_Fields_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Field's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()

    def test_fields_gift(self):
        self.plr.coin = 0
        self.plr.action = 0
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 1 + 2)  # Boon + Bard
            self.assertEqual(self.plr.actions.get(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
