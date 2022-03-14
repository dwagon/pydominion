#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Delve(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "+1 Buy. Gain a Silver."
        self.name = "Delve"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        player.gain_card("Silver")
        player.addBuys()


###############################################################################
class Test_Delve(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Delve"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Delve"]

    def test_play(self):
        """Perform a Delve"""
        self.plr.addCoin(2)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertEqual(self.plr.get_buys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
