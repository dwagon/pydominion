#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Cellar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = (
            "+1 Action; Discard any number of cards. +1 card per card discarded."
        )
        self.name = "Cellar"
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        to_discard = player.plr_discard_cards(
            0,
            any_number=True,
            prompt="Discard any number of cards and gain one per card discarded",
        )
        if to_discard:
            player.pickup_cards(len(to_discard))


###############################################################################
class TestCellar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cellar"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.ccard = self.g.get_card_from_pile("Cellar")

    def test_none(self):
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Silver")
        self.plr.add_card(self.ccard, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)

    def test_one(self):
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Silver")
        self.plr.piles[Piles.DECK].set("Province", "Gold")
        self.plr.add_card(self.ccard, Piles.HAND)
        self.plr.test_input = ["discard estate", "finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Province")
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
