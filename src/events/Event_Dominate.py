#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Dominate(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "Gain a Province. If you do, +9VP."
        self.name = "Dominate"
        self.cost = 14

    def special(self, game, player):
        c = player.gainCard('Province')
        if c:
            player.addScore('Dominate', 9)


###############################################################################
class Test_Dominate(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Dominate'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events['Dominate']

    def test_play(self):
        """ Perform a Dominate """
        self.plr.addCoin(14)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertEqual(self.plr.getScoreDetails()['Dominate'], 9)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
