#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Horsetraders(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+1 Buy. +3 Coins. Discard 2 cards.
        When another player plays an Attack card, you may set this aside from your hand.
        If you do, then at the start of your next turn, +1 Card and return this to your hand."""
        self.name = "Horse Traders"
        self.buys = 1
        self.coin = 3
        self.cost = 4

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)

    def todo(self):  # TODO
        """When another player plays an Attack card, you may set
        this aside from your hand.  If you do, then at the start
        of your next turn, +1 Card and return this to your hand."""


###############################################################################
class Test_Horsetraders(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Horse Traders"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Horse Traders")

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
