#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Delve(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "+1 Buy. Gain a Silver."
        self.name = "Delve"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        player.gainCard('Silver')
        player.addBuys()


###############################################################################
class Test_Delve(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Delve'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Delve']

    def test_play(self):
        """ Perform a Delve """
        self.plr.addCoin(2)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF