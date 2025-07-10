#!/usr/bin/env python

import unittest

from dominion import Boon
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Boon_Winds_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+2 Cards; Discard 2 cards."
        self.name = "The Wind's Gift"
        self.cards = 2
        self.purchasable = False

    def special(self, game, player):
        player.plr_discard_cards(num=2)


###############################################################################
class Test_Winds_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Wind's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g.get_card_from_pile("Bard")

    def test_winds_gift(self):
        self.plr.piles[Piles.HAND].set("Duchy", "Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard Duchy", "Discard Gold", "Finish Selecting"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Duchy"])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
