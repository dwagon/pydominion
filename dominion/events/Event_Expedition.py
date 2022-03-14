#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Expedition(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Draw 2 extra cards for your next turn"
        self.name = "Expedition"
        self.cost = 3

    def special(self, game, player):
        player.newhandsize += 2


###############################################################################
class Test_Expedition(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Expedition"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Expedition"]

    def test_playonce(self):
        """Use Expedition once"""
        self.plr.coin = 3
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.get_coins(), 0)
        self.plr.end_turn()
        self.assertEqual(self.plr.hand.size(), 7)

    def test_playtwice(self):
        """Use Expedition twice"""
        self.plr.coin = 7
        self.plr.addBuys(1)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.get_coins(), 4)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.get_buys(), 0)
        self.plr.end_turn()
        self.assertEqual(self.plr.hand.size(), 9)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
