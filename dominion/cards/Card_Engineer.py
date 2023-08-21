#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Engineer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """Gain a card costing up to 4 Coin.
        You may trash this. If you do, gain a card costing up to 4 Coin."""
        self.name = "Engineer"
        self.debtcost = 4
        self.coin = 1

    def special(self, game, player):
        player.plr_gain_card(4)
        trash = player.plr_choose_options(
            "Trash the Engineer?",
            ("Keep the engineer", False),
            ("Trash to gain a card costing up to 4", True),
        )
        if trash and self.location != "trash":
            player.trash_card(self)
            player.plr_gain_card(4)


###############################################################################
class TestEngineer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Engineer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Engineer"].remove()

    def test_play_trash(self):
        """Play an Engineer and trash it"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Silver", "Trash", "Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Engineer", self.g.trashpile)

    def test_play_keep(self):
        """Play an Engineer and keep it"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Silver", "Keep"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Engineer", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Engineer", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
