#!/usr/bin/env python

import unittest
from collections import defaultdict
from Project import Project


###############################################################################
class Project_SinisterPlot(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, add a token here, or remove your tokens here for +1 Card each."
        self.name = "Sinister Plot"
        self.cost = 4
        self._token = defaultdict(int)

    def hook_startTurn(self, game, player):
        ch = player.plrChooseOptions(
                "Sinister Plot Action? ",
                ("Add a token here?", True),
                ("Remove {} tokens for {} cards?".format(self._token[player.name], self._token[player.name]), False)
                )
        if ch:
            self._token[player.name] += 1
        else:
            player.pickupCards(self._token[player.name])
            self._token[player.name] = 0


###############################################################################
class Test_SinisterPlot(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Sinister Plot'], initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_add(self):
        self.plr.assign_project('Sinister Plot')
        self.plr.test_input = ['Add a token']
        self.plr.startTurn()
        self.assertEqual(self.plr.projects[0]._token[self.plr.name], 1)

    def test_use(self):
        self.plr.assign_project('Sinister Plot')
        self.plr.projects[0]._token[self.plr.name] = 2
        self.plr.test_input = ['Remove']
        self.plr.startTurn()
        self.assertEqual(self.plr.projects[0]._token[self.plr.name], 0)
        self.assertEqual(self.plr.handSize(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF