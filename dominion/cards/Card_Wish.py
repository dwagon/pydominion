#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Wish(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Action; Return this to its pile. If you did, gain a card to your hand costing up to 6."
        self.name = "Wish"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cost = 0
        self.numcards = 12

    def special(self, game, player):
        return_card = player.plr_choose_options(
            "Return this to gain a card to your hand costing up to 6",
            ("Return", True),
            ("Keep", False),
        )
        if return_card:
            game["Wish"].add(self)
            player.played.remove(self)
            player.plr_gain_card(cost=6)


###############################################################################
class TestWish(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wish"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Wish"].remove()

    def test_return(self):
        num_wishes = len(self.g["Wish"])
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Return", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertNotIn("Wish", self.plr.played)
        self.assertNotIn("Wish", self.plr.discardpile)
        self.assertEqual(len(self.g["Wish"]), num_wishes + 1)

    def test_keep(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.discardpile)
        self.assertIn("Wish", self.plr.played)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
