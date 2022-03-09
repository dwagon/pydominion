#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Gardens(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.DOMINION
        self.desc = "numcards / 10 VP"
        self.name = "Gardens"
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """Worth 1VP for every 10 cards in your deck rounded down"""
        numcards = len(player.allCards())
        return int(numcards / 10)


###############################################################################
class Test_Gardens(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Gardens"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_score_0(self):
        self.plr.setHand("Gardens", "Copper", "Copper")
        self.plr.setDeck("Copper", "Copper", "Copper")
        self.plr.setDiscard("Copper", "Copper", "Copper")
        score = self.plr.getScoreDetails()
        self.assertEqual(score["Gardens"], 0)

    def test_score_1(self):
        self.plr.setHand("Gardens", "Copper", "Copper")
        self.plr.setDeck("Copper", "Copper", "Copper", "Copper")
        self.plr.setDiscard("Copper", "Copper", "Copper")
        score = self.plr.getScoreDetails()
        self.assertEqual(score["Gardens"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
