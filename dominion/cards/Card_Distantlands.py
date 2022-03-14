#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Distantlands(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE, Card.TYPE_VICTORY]
        self.base = Game.ADVENTURE
        self.desc = "Worth 4 VP if on your tavern mat at the end of the game, else 0"
        self.name = "Distant Lands"
        self.cost = 5
        self.callable = False
        self.counted = False

    def special_score(self, game, player):
        """Worth 4 VP if on your tavern mat; else 0"""
        score = 0
        if game.gameover:
            for c in player.reserve:
                if c.name == "Distant Lands" and not c.counted:
                    c.counted = True
                    score += 4
        return score


###############################################################################
class Test_Distantlands(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Distant Lands"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Distant Lands"].remove()

    def test_play(self):
        """Play a distant lands"""
        self.plr.set_hand()
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertIsNotNone(self.plr.in_reserve("Distant Lands"))

    def test_notonmat(self):
        self.plr.set_hand("Distant Lands")
        self.g.gameover = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 0)

    def test_onmat(self):
        """Distant lands on mat"""
        self.plr.set_reserve("Distant Lands")
        self.g.gameover = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 4)

    def test_onmat_twice(self):
        """Two Distant lands on mat"""
        self.plr.set_reserve("Distant Lands", "Distant Lands")
        self.g.gameover = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
