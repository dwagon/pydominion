#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Harem(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_VICTORY]
        self.base = Game.INTRIGUE
        self.name = "Harem"
        self.coin = 2
        self.victory = 2
        self.cost = 6

    def desc(self, player):
        if player.phase == "buy":
            return "+2 coin; 2 VPs"
        return "+2 coin"


###############################################################################
class Test_Harem(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Harem"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Harem"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play a Harem"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_score(self):
        """Score the harem"""
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc["Harem"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
