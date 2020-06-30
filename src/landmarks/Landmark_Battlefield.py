#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Battlefield(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.name = "Battlefield"
        self._vp = 0

    def desc(self, player):
        return "When you gain a Victory card, take 2VP from here. (%d left)" % self._vp

    def hook_gainCard(self, game, player, card):
        if card.isVictory() and self._vp >= 0:
            self._vp -= 2
            player.output("Gained 2VP from Battlefield")
            player.addScore('Battlefield', 2)

    def setup(self, game):
        self._vp = 6 * game.numplayers


###############################################################################
class Test_Battlefield(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Battlefield'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Battlefield """
        self.plr.buyCard(self.g['Duchy'])
        self.assertEqual(self.plr.getScoreDetails()['Battlefield'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
