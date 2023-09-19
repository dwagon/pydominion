#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Amulet(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
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
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_coin(self):
        """Play an amulet with coin"""
        self.plr.test_input = ["coin", "coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_silver(self):
        """Play an amulet with coin"""
        self.plr.test_input = ["silver", "silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_trash(self):
        """Play an amulet with trash"""
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash", "duchy", "finish", "trash", "1", "finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
