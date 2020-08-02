#!/usr/bin/env python

import unittest
import Game
from State import State


###############################################################################
class State_Twice_Miserable(State):
    def __init__(self):
        State.__init__(self)
        self.cardtype = 'state'
        self.base = 'nocturne'
        self.desc = "-4 VP"
        self.name = "Twice Miserable"
        self.victory = -4


###############################################################################
class Test_Twice_Miserable(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.state = self.g.states['Twice Miserable']

    def test_have(self):
        self.plr.assign_state('Twice Miserable')
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Twice Miserable'], -4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
