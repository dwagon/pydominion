#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Duke(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.INTRIGUE
        self.desc = "Worth 1 VP per duchy"
        self.name = "Duke"
        self.playable = False
        self.cost = 5

    def special_score(self, game, player):
        """Worth 1VP per Duchy you have"""
        vp = 0
        for c in player.allCards():
            if c.name == "Duchy":
                vp += 1
        return vp


###############################################################################
class Test_Duke(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Duke"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_score(self):
        self.plr.setDeck("Duchy", "Duchy", "Estate")
        self.plr.setHand("Silver")
        self.plr.setDiscard("Duke")
        sc = self.plr.getScore()
        self.assertEqual(sc, 9)  # 3 per duchy, 1 per estate, 2 from duke


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
