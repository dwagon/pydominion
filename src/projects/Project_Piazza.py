#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Piazza(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, reveal the top card of your deck. If it's an Action, play it."
        self.name = "Piazza"
        self.cost = 5

    def hook_startTurn(self, game, player):
        c = player.nextCard()
        if c.isAction():
            player.output("Piazaa playing {}".format(c.name))
            player.addCard(c, 'hand')
            player.playCard(c)
        else:
            player.output("Piazza revealed {} but it isn't an action - putting back".format(c.name))
            player.addCard(c, 'topdeck')


###############################################################################
class Test_Piazza(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Piazza'], initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Moat')
        self.plr.assign_project('Piazza')
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inPlayed('Moat'))
        self.assertEqual(self.plr.handSize(), 5 + 2)

    def test_noaction(self):
        self.plr.setDeck('Province', 'Silver')
        self.plr.assign_project('Piazza')
        self.plr.startTurn()
        self.assertEqual(self.plr.deck[-1].name, 'Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
