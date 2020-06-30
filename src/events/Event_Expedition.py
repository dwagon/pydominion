#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Expedition(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Draw 2 extra cards for your next turn"
        self.name = "Expedition"
        self.cost = 3

    def special(self, game, player):
        player.newhandsize += 2


###############################################################################
class Test_Expedition(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Expedition'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Expedition']

    def test_playonce(self):
        """ Use Expedition once """
        self.plr.coin = 3
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.plr.endTurn()
        self.assertEqual(self.plr.handSize(), 7)

    def test_playtwice(self):
        """ Use Expedition twice """
        self.plr.coin = 7
        self.plr.addBuys(1)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.getCoin(), 4)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getBuys(), 0)
        self.plr.endTurn()
        self.assertEqual(self.plr.handSize(), 9)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
