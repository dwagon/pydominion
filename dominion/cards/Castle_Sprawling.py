#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_SprawlingCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 8
        self.desc = """4VP. When you gain this, gain a Duchy or 3 Estates."""
        self.victory = 4
        self.name = "Sprawling Castle"

    def hook_gain_this_card(self, game, player):
        ch = player.plr_choose_options(
            "Gain a Duchy or 3 Estates",
            ("Gain a Duchy", "duchy"),
            ("Gain 3 Estates", "estates"),
        )
        if ch == "duchy":
            player.gain_card("Duchy")
        else:
            for _ in range(3):
                player.gain_card("Estate")


###############################################################################
class Test_SprawlingCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=2, initcards=["Castles"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        """Play a sprawling castle"""
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Sprawling Castle":
                break
        self.plr.add_card(self.card, Piles.HAND)
        self.assertEqual(self.plr.get_score_details()["Sprawling Castle"], 4)

    def test_gain_duchy(self):
        """Gain duchy through Sprawling Castle"""
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Opulent Castle":  # One before Sprawling
                break
        self.plr.test_input = ["duchy"]
        self.plr.gain_card("Castles")
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1 + 1)

    def test_gain_estate(self):
        """Gain estates through Sprawling Castle"""
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Opulent Castle":  # One before Sprawling
                break
        self.plr.test_input = ["estates"]
        self.plr.gain_card("Castles")
        self.assertNotIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.g.print_state()
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
