#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Plunder"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Plunder(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+2 Coin, +1VP"""
        self.name = "Plunder"
        self.coin = 2
        self.victory = 1
        self.cost = 5
        self.pile = "Encampment"


###############################################################################
class TestPlunder(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Encampment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Encampment", "Plunder")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a rebuild"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.get_score_details()["Plunder"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
