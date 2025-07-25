#!/usr/bin/env python

import unittest

from dominion import Boon
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Boon_Rivers_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card at the end of this turn."
        self.name = "The River's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.newhandsize += 1


###############################################################################
class TestRivers_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The River's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g.get_card_from_pile("Bard")

    def test_winds_gift(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
