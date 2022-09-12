#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Amulet(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = "Now and next turn - Choose 1: +1 Coin, trash card, gain silver"
        self.name = "Amulet"
        self.cost = 3

    def special(self, game, player):
        self.amulet_special(game, player)

    def duration(self, game, player):
        self.amulet_special(game, player)

    def amulet_special(self, game, player):
        """Now and at the start of your next turn, choose one: +1 Coin;
        or trash a card from your hand; or gain a Silver"""
        choice = player.plr_choose_options(
            "Pick one",
            ("Gain a coin", "coin"),
            ("Trash a card", "trash"),
            ("Gain a silver", "silver"),
        )
        if choice == "coin":
            player.coins.add(1)
        if choice == "trash":
            player.plr_trash_card(num=1)
        if choice == "silver":
            player.gain_card("Silver")


###############################################################################
class Test_Amulet(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Amulet"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Amulet"].remove()
        self.plr.hand.set("Duchy")
        self.plr.add_card(self.card, "hand")

    def test_play_coin(self):
        """Play an amulet with coin"""
        self.plr.test_input = ["coin", "coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.discardpile)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.discardpile)

    def test_play_silver(self):
        """Play an amulet with coin"""
        self.plr.test_input = ["silver", "silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Silver", self.plr.discardpile)

    def test_play_trash(self):
        """Play an amulet with trash"""
        tsize = self.g.trashpile.size()
        self.plr.test_input = ["trash", "duchy", "finish", "trash", "1", "finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Silver", self.plr.discardpile)
        self.assertIn("Duchy", self.g.trashpile)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Silver", self.plr.discardpile)
        self.assertEqual(self.g.trashpile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
