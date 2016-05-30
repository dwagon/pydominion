#!/usr/bin/env python

import unittest
import Game


###############################################################################
class TestPick_to_discard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, bot=True)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_no_discard(self):
        """ Test pick_to_discard with no discard requirement """
        self.plr.setHand('Estate', 'Copper', 'Copper', 'Gold')
        card = self.plr.pick_to_discard(0)
        self.assertEqual(len(card), 0)

    def test_not_treasure(self):
        """ Test pick_to_discard with a non-treasure to discard """
        self.plr.setHand('Estate', 'Copper', 'Copper', 'Gold')
        card = self.plr.pick_to_discard(1)
        self.assertEqual(len(card), 1)
        self.assertEqual(card[0].name, 'Estate')

    def test_treasure(self):
        """ Test pick_to_discard when it has to drop a treasure"""
        self.plr.setHand('Estate', 'Copper', 'Silver', 'Gold')
        cards = self.plr.pick_to_discard(2)
        self.assertEqual(len(cards), 2)
        cardnames = [c.name for c in cards]

        self.assertIn('Estate', cardnames)
        self.assertIn('Copper', cardnames)

    def test_good_treasure(self):
        """ Test pick_to_discard when it has to drop good treasures"""
        self.plr.setHand('Gold', 'Gold', 'Silver', 'Gold')
        cards = self.plr.pick_to_discard(2)
        self.assertEqual(len(cards), 2)
        cardnames = [c.name for c in cards]

        self.assertIn('Silver', cardnames)
        self.assertIn('Gold', cardnames)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
