#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Vineyard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "num action cards / 3 VP"
        self.name = "Vineyard"
        self.playable = False
        self.cost = 0
        self.required_cards = ["Potion"]
        self.potcost = True

    def special_score(self, game, player):
        """Worth 1VP for every 3 action cards in your deck rounded down"""
        score = 0
        for c in player.all_cards():
            if c.isAction():
                score += 1
        return int(score / 3)


###############################################################################
class Test_Vineyard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Vineyard", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_scoreOne(self):
        self.plr.piles[Piles.HAND].set("Vineyard")
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.piles[Piles.DISCARD].set("Moat", "Moat", "Moat", "Moat")
        self.assertEqual(self.plr.get_score_details()["Vineyard"], 1)

    def test_scoreTwo(self):
        self.plr.piles[Piles.HAND].set("Vineyard")
        self.plr.piles[Piles.DECK].set("Vineyard")
        self.plr.piles[Piles.DISCARD].set("Moat", "Moat", "Moat", "Moat", "Moat", "Moat")
        self.assertEqual(self.plr.get_score_details()["Vineyard"], 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
