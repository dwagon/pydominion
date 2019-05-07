#!/usr/bin/env python

import unittest
from State import State


###############################################################################
class State_Miserable(State):
    def __init__(self):
        State.__init__(self)
        self.cardtype = 'state'
        self.base = 'nocturne'
        self.desc = "-2 VP"
        self.name = "Miserable"
        self.victory = -2


###############################################################################
class Test_Miserable(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.state = self.g.states['Miserable']

    def test_have(self):
        self.plr.assign_state('Miserable')
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Miserable'], -2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
