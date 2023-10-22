#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Boon_Mountains_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a silver"
        self.name = "The Mountain's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.gain_card("Silver")


###############################################################################
class Test_Mountains_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Mountain's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g.get_card_from_pile("Bard")

    def test_mountains_gift(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
