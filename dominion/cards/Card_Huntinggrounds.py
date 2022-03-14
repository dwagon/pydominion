#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Huntinggrounds(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+4 Cards; When you trash this, gain a Duchy or 3 Estates."""
        self.name = "Hunting Grounds"
        self.cards = 4
        self.cost = 6

    def hook_trashThisCard(self, game, player):
        choice = player.plr_choose_options(
            "What to gain?", ("Gain a duchy", "duchy"), ("Gain 3 Estates", "estates")
        )
        if choice == "duchy":
            player.gain_card("Duchy")
        if choice == "estates":
            for _ in range(3):
                player.gain_card("Estate")


###############################################################################
class Test_Huntinggrounds(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initcards=["Hunting Grounds"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hunting Grounds"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Hunting Ground"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 4)

    def test_trash_estate(self):
        """Trash a hunting ground and gain estates"""
        self.plr.test_input = ["Estates"]
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 3)
        self.assertIsNotNone(self.plr.in_discard("Estate"))

    def test_trash_duchy(self):
        """Trash a hunting ground and gain duchy"""
        self.plr.test_input = ["Duchy"]
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIsNotNone(self.plr.in_discard("Duchy"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
