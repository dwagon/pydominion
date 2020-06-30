#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Alliance(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'menagerie'
        self.desc = "Gain a Province, a Duchy, an Estate, a Gold, a Silver, and a Copper."
        self.name = "Alliance"
        self.cost = 10

    def special(self, game, player):
        player.gainCard('Province')
        player.gainCard('Duchy')
        player.gainCard('Estate')
        player.gainCard('Gold')
        player.gainCard('Silver')
        player.gainCard('Copper')


###############################################################################
class Test_Alliance(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alliance'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Alliance']

    def test_play(self):
        """ Perform a Alliance """
        self.plr.addCoin(10)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
