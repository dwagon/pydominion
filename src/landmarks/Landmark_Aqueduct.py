#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Aqueduct(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When you gain a Treasure, move 1 VP from its pile to this. When you gain a Victory card, take the VP from this."""
        self.name = "Aqueduct"
        self._goldvp = 8
        self._silvervp = 8
        self._vp = 0

    def hook_gainCard(self, game, player, card):
        if card.name == 'Gold':
            if self._goldvp:
                self._goldvp -= 1
                self._vp += 1
                player.output("%d VP left on Gold; %d VP on Aqueduct" % (self._goldvp, self._vp))
        if card.name == 'Silver':
            if self._silvervp:
                self._silvervp -= 1
                self._vp += 1
                player.output("%d VP left on Silver; %d VP on Aqueduct" % (self._silvervp, self._vp))
        print "card=%s" % card
        if card.isVictory():
            player.output("Gained %d VP from Aqueduct" % self._vp)
            player.addScore('Aqueduct', self._vp)
            self._vp = 0


###############################################################################
class Test_Aqueduct(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Aqueduct'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Aqueduct gaining Silver"""
        self.plr.buyCard(self.g["Silver"])
        self.assertEqual(self.g.landmarks['Aqueduct']._vp, 1)
        self.assertEqual(self.g.landmarks['Aqueduct']._silvervp, 7)
        self.plr.buyCard(self.g["Duchy"])
        self.g.print_state()
        self.assertEqual(self.plr.getScoreDetails()['Aqueduct'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
