#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Silkroad(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = "num victory cards / 4 VP"
        self.name = "Silk Road"
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """Worth 1VP for every 4 victory cards in your deck rounded down"""
        score = 0
        for c in player.all_cards():
            if c.isVictory():
                score += 1
        return int(score / 4)


###############################################################################
class Test_Silkroad(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Silk Road"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_scoreOne(self):
        self.plr.piles[Piles.HAND].set("Silk Road")
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.piles[Piles.DISCARD].set("Estate", "Estate", "Estate", "Estate")
        self.assertEqual(self.plr.get_score_details()["Silk Road"], 1)

    def test_scoreTwo(self):
        """Score for having two silk roads worth two each"""
        self.plr.piles[Piles.HAND].set("Silk Road", "Estate")
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Silk Road")
        self.plr.piles[Piles.DISCARD].set("Estate", "Estate", "Estate", "Estate", "Estate")
        self.assertEqual(self.plr.get_score_details()["Silk Road"], 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
