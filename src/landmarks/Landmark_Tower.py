#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Tower(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = "When scoring, 1VP per non-Victory card you have from an empty Supply pile."
        self.name = "Tower"

    def hook_end_of_game(self, game, player):
        empties = [1 for st in game.cardpiles if game[st].isEmpty() and not game[st].isVictory()]
        for emp in empties:
            for card in player.allCards():
                if card.anem == emp.name:
                    player.addScore('Tower', 1)


###############################################################################
class Test_Tower(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Tower'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Tower """
        self.plr.setDiscard('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Tower'], 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
