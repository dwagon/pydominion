#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Arena(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Arena"

    def desc(self, player):
        return "At the start of your Buy phase, you may discard an Action card. If you do, take 2VP from here. (%d left)" % self._vp

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_preBuy(self, game, player):
        if self._vp <= 0:
            return
        actions = []
        for card in player.hand:
            if card.isAction():
                actions.append(card)
        if not actions:
            return
        disc = player.plrDiscardCards(prompt="Arena: Discard an action to gain 2VP", cardsrc=actions)
        if disc:
            player.output("Gained 2 VP from Arena")
            self._vp -= 2
            player.addScore('Arena', 2)


###############################################################################
class Test_Arena(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Arena'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Arena """
        self.plr.setHand('Moat')
        self.plr.test_input = ['Discard Moat', 'End Phase']
        self.plr.buy_phase()
        self.assertEqual(self.plr.getScoreDetails()['Arena'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
