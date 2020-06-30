#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_performEvent(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Raid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
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
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alms', 'Expedition', 'Raid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_events(self):
        self.plr.coin = 4
        output, index = self.plr.eventSelection(3)
        self.assertEqual(index, 6)
        self.assertEqual(len(output), 3)
        num_affordable = 0
        num_notaff = 0
        for i in output:
            if i['action'] == 'event':
                num_affordable += 1
            elif i['action'] is None:
                num_notaff += 1
            else:   # pragma: no coverage
                self.fail("Unexpected action %s in %s" % (i['action'], i))
        self.assertEqual(num_affordable, 2)
        self.assertEqual(num_notaff, 1)


###############################################################################
class Test_eventRandom(unittest.TestCase):
    def test_none(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.assertEqual(len(self.g.events), 0)

    def test_specify(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alms', 'Raid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.assertEqual(len(self.g.events), 2)
        self.assertIn('Alms', self.g.events)
        self.assertIn('Raid', self.g.events)

    def test_random(self):
        self.g = Game.Game(quiet=True, numplayers=1, numevents=2)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.assertEqual(len(self.g.events), 2)

    def test_both(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alms'], numevents=2)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.assertEqual(len(self.g.events), 2)
        self.assertIn('Alms', self.g.events)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
