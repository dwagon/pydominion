#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Hero(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+2 Coin, Gain a Treasure; Discard to replace with Champion"
        self.name = "Hero"
        self.purchasable = False
        self.coin = 2
        self.cost = 5
        self.numcards = 5

    def special(self, game, player):
        """Gain a treasure"""
        player.plr_gain_card(cost=None, types={Card.CardType.TREASURE: True})

    def hook_discard_this_card(self, game, player, source):
        """Replace with Champion"""
        player.replace_traveller(self, "Champion")


###############################################################################
class Test_Hero(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, initcards=["Page"], badcards=["Fool's Gold"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hero"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_hero(self):
        """Play a hero"""
        self.plr.test_input = ["get gold"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 2)
            self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
