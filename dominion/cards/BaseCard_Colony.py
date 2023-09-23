#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Colony(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+10 VP"
        self.basecard = True
        self.name = "Colony"
        self.playable = False
        self.cost = 11
        self.victory = 10

    @classmethod
    def calc_numcards(cls, game):
        if game.numplayers == 2:
            return 8
        return 12


###############################################################################
class Test_Colony(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(prosperity=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Colony")
        self.plr.add_card(self.card, Piles.HAND)

    def test_score(self):
        """Score a colony"""
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Colony"], 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
