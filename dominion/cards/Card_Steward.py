#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Steward(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "Choose: +2 cards, +2 coin, trash 2 cards"
        self.name = "Steward"
        self.cost = 3

    def special(self, game, player):
        """Choose one: +2 Cards; or +2 coin, or trash 2 cards from your hand"""
        choice = player.plr_choose_options(
            "Choose one?",
            ("+2 cards", "cards"),
            ("+2 coin", "coin"),
            ("Trash 2", "trash"),
        )
        if choice == "cards":
            player.pickup_cards(2)
            return
        if choice == "coin":
            player.coins.add(2)
            return
        if choice == "trash":
            player.output("Trash two cards")
            num = min(2, player.piles[Piles.HAND].size())
            player.plr_trash_card(num=num, force=True)
            return


###############################################################################
class Test_Steward(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Steward"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Steward"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_cards(self):
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_gold(self):
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_trash(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["2", "1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)

    def test_trash_smallhand(self):
        """Trash two when there are less than two to trash"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["2", "1", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
