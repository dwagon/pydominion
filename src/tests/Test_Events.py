#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_performEvent(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['raid'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Raid']

    def test_perform(self):
        """ Perform an event """
        self.plr.buys = 1
        self.plr.coin = 5
        sc = self.plr.performEvent(self.card)
        self.assertTrue(sc)
        self.assertEqual(self.plr.getBuys(), 0)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_no_buy(self):
        """ Perform an event without a buy """
        self.plr.buys = 0
        self.plr.coin = 2
        sc = self.plr.performEvent(self.card)
        self.assertFalse(sc)
        self.assertEqual(self.plr.getBuys(), 0)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_no_coin(self):
        """ Perform an event without enough coins """
        self.plr.coin = 2
        self.plr.buys = 1
        sc = self.plr.performEvent(self.card)
        self.assertFalse(sc)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
class Test_eventSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['alms', 'expedition', 'raid'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_events(self):
        self.plr.coin = 4
        output, index = self.plr.eventSelection(3)
        self.assertEquals(index, 5)
        self.assertEquals(len(output), 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
