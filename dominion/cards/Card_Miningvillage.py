#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Miningvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+1 card, +2 actions, trash self for +2 coin"
        self.name = "Mining Village"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        """You may trash this card immediately. If you do +2 coin"""
        trash = player.plrChooseOptions(
            "Choose one",
            ("Do nothing", False),
            ("Trash mining village for +2 coin", True),
        )
        if trash:
            player.output("Trashing mining village")
            player.add_coins(2)
            player.trash_card(self)


###############################################################################
class Test_Miningvillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Mining Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mining Village"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Mining Village"""
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertIsNone(self.g.in_trash("Mining Village"))
        self.assertEqual(self.plr.played[-1].name, "Mining Village")

    def test_trash(self):
        """Trash the mining village"""
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertTrue(self.plr.played.is_empty())
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIsNotNone(self.g.in_trash("Mining Village"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
