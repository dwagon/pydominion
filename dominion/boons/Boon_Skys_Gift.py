#!/usr/bin/env python

import unittest

from dominion import Boon, Card, Game, Piles


###############################################################################
class Boon_Skys_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "You may discard 3 cards to gain a Gold."
        self.name = "The Sky's Gift"
        self.purchasable = False

    def special(self, game, player):
        if player.piles[Piles.HAND].is_empty():
            player.output("No cards to discard")
            return
        dc = player.plr_discard_cards(
            any_number=True, prompt="Discard 3 cards to gain a Gold"
        )
        if dc is None:
            return
        if len(dc) >= 3:
            player.gain_card("Gold")
            player.output("Gained a Gold")


###############################################################################
class TestSkysGift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        my_boon = None
        for b in self.g.boons:
            if b.name == "The Sky's Gift":
                my_boon = b
                break
        self.g.boons = [my_boon]
        self.card = self.g.get_card_from_pile("Bard")

    def test_sky_gift(self):
        """Discard 3 cards to gain a gold"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Copper", "Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])

    def test_sky_no_gift(self):
        """Discard less than three cards to gain nothing"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Copper", "Estate", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_sky_no_discards(self):
        """Discard when no cards available"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
