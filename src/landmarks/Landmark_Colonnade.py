#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Colonnade(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.name = "Colonnade"

    def desc(self, player):
        if self._vp:
            return "When you buy an Action card, if you have a copy of it in play, take 2VP from here. %d left" % self._vp
        else:
            return "No VP left"

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_buyCard(self, game, player, card):
        if not card.isAction():
            return
        if not self._vp:
            return
        if player.inPlayed(card.name):
            self._vp -= 2
            player.addScore('Colonnade', 2)
            player.output("Gained 2VP from Colonnade")


###############################################################################
class Test_Colonnade(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Colonnade'], initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_play(self):
        """ Test Colonnade"""
        self.plr.setPlayed('Moat')
        self.plr.buyCard(self.g['Moat'])
        self.assertEqual(self.plr.getScoreDetails()['Colonnade'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
