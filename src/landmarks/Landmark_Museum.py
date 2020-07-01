#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Museum(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = "When scoring, 2VP per differently named card you have."
        self.name = "Museum"

    def hook_end_of_game(self, game, player):
        c = set()
        for card in player.allCards():
            c.add(card.name)
        player.addScore('Museum', len(c) * 2)


###############################################################################
class Test_Museum(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Museum'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Museum """
        self.plr.setHand('Copper', 'Estate')
        self.plr.setDiscard('Gold', 'Silver', 'Copper')
        self.plr.setDeck('Gold', 'Moat', 'Moat')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Museum'], 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
