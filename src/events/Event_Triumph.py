#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Triumph(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "Gain an Estate. If you did, +1VP per card you've gained this turn."
        self.name = "Triumph"
        self.debtcost = 5

    def special(self, game, player):
        new = player.gainCard('Estate')
        if new:
            vps = len(player.stats['gained'])
            player.addScore('Triumph', vps)


###############################################################################
class Test_Triumph(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Triumph'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.event = self.g.events['Triumph']

    def test_triumph(self):
        """ Use Triumph"""
        self.plr.gainCard('Copper')
        self.plr.performEvent(self.event)
        self.assertIsNotNone(self.plr.inDiscard('Estate'))
        scores = self.plr.getScoreDetails()
        self.assertEqual(scores['Triumph'], 2)
        self.assertEqual(self.plr.debt, 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
