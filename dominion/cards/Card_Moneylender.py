#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Moneylender(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash a copper from hand for +3 coin"
        self.name = "Money Lender"
        self.cost = 4

    def special(self, game, player):
        """Trash a copper card from your hand. If you do +3 coin"""
        copper = player.hand["Copper"]
        if not copper:
            player.output("No coppers in hand")
            return
        player.output("Trash a copper to gain +3 coin")
        trash = player.plr_choose_options(
            "Trash a copper?", ("Don't trash a copper", False), ("Trash a copper", True)
        )
        if trash:
            player.trash_card(copper)
            player.coins.add(3)


###############################################################################
class Test_Moneylender(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Money Lender"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Money Lender"].remove()

    def test_nocopper(self):
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_trash_copper(self):
        tsize = self.g.trashpile.size()
        self.plr.test_input = ["1"]
        self.plr.hand.set("Copper", "Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trashpile)
        self.assertEqual(self.g.trashpile.size(), tsize + 1)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_dont_trash_copper(self):
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Copper", "Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
