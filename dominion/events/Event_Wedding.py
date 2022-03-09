#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Wedding(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "+1VP, Gain a Gold."
        self.name = "Wedding"
        self.cost = 4
        self.debtcost = 3

    def special(self, game, player):
        player.addScore("Wedding", 1)
        player.gainCard("Gold")


###############################################################################
class Test_Wedding(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Wedding"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Wedding"]

    def test_play(self):
        """Perform a Wedding"""
        self.plr.addCoin(4)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertEqual(self.plr.debt, 3)
        self.assertEqual(self.plr.getScoreDetails()["Wedding"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
