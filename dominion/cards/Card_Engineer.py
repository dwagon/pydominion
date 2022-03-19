#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Engineer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = """Gain a card costing up to 4 Coin.
        You may trash this. If you do, gain a card costing up to 4 Coin."""
        self.name = "Engineer"
        self.debtcost = 4
        self.coin = 1

    def special(self, game, player):
        player.plr_gain_card(4)
        trash = player.plr_choose_options(
            "Trash the Engineer?",
            ("Keep the enginner", False),
            ("Trash to gain a card costing up to 4", True),
        )
        if trash:
            player.trash_card(self)
            player.plr_gain_card(4)


###############################################################################
class Test_Engineer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Engineer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Engineer"].remove()

    def test_play_trash(self):
        """Play an Engineer and trash it"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Get Silver", "Trash", "Moat"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Moat"))
        self.assertIsNotNone(self.g.in_trash("Engineer"))

    def test_play_keep(self):
        """Play an Engineer and keep it"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Get Silver", "Keep"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_played("Engineer"))
        self.assertIsNone(self.g.in_trash("Engineer"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
