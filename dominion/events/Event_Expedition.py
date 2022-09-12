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
        self.g = Game.TestGame(numplayers=1, eventcards=["Expedition"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Expedition"]

    def test_playonce(self):
        """Use Expedition once"""
        self.plr.coins.set(3)
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.assertEqual(self.plr.hand.size(), 7)

    def test_playtwice(self):
        """Use Expedition twice"""
        self.plr.coins.set(7)
        self.plr.add_buys(1)
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.coins.get(), 4)
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.get_buys(), 0)
        self.plr.end_turn()
        self.assertEqual(self.plr.hand.size(), 9)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
