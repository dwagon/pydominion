#!/usr/bin/env python

import unittest
import Game
import Card
from Event import Event


###############################################################################
class Event_Banquet(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Gain 2 Coppers and a non-Victory card costing up to 5"
        self.name = "Banquet"
        self.cost = 3

    def special(self, game, player):
        for _ in range(2):
            player.gainCard('Copper')
        player.plrGainCard(5, types={Card.TYPE_ACTION: True, Card.TYPE_TREASURE: True, Card.TYPE_VICTORY: False})


###############################################################################
class Test_Banquet(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Banquet'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Banquet']

    def test_event(self):
        """ Use the event """
        self.plr.test_input = ['Get Silver']
        self.plr.addCoin(3)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard('Copper'))
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertEqual(self.plr.discardpile.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
