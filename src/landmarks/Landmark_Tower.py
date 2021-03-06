#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Tower(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "When scoring, 1VP per non-Victory card you have from an empty Supply pile."
        self.name = "Tower"

    def hook_end_of_game(self, game, player):
        player.addScore('Tower', 0)
        empties = [st for st in game.cardpiles if game[st].is_empty() and not game[st].isVictory()]
        for emp in empties:
            for card in player.allCards():
                if card.name == emp:
                    player.addScore('Tower', 1)


###############################################################################
class Test_Tower(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Tower'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_none(self):
        """ Use Tower """
        self.plr.setHand('Moat', 'Moat')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Tower'], 0)

    def test_one(self):
        self.plr.setHand('Moat', 'Moat')
        while True:
            c = self.g['Moat'].remove()
            if not c:
                break
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Tower'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
