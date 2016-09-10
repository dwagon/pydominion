#!/usr/bin/env python

import unittest
from Landmark import Landmark
from collections import defaultdict


###############################################################################
class Landmark_Orchard(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = "When scoring, 4VP per differently named Action card you have 3 or more copies of."
        self.name = "Orchard"

    def hook_end_of_game(self, game, player):
        actions = defaultdict(int)
        for card in player.allCards():
            if card.isAction():
                actions[card.name] += 1
        score = sum([4 for x in actions.values() if x > 3])
        player.addScore('Orchard', score)


###############################################################################
class Test_Orchard(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Orchard'], initcards=['Moat', 'Militia'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Orchard """
        self.plr.setDiscard('Moat', 'Moat', 'Militia', 'Duchy')
        self.plr.setDeck('Moat', 'Moat', 'Copper', 'Duchy')
        self.plr.setHand('Moat', 'Militia', 'Copper', 'Copper', 'Duchy')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Orchard'], 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF