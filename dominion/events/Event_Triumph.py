#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Triumph(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "Gain an Estate. If you did, +1VP per card you've gained this turn."
        self.name = "Triumph"
        self.debtcost = 5

    def special(self, game, player):
        new = player.gain_card("Estate")
        if new:
            vps = len(player.stats["gained"])
            player.add_score("Triumph", vps)


###############################################################################
class Test_Triumph(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Triumph"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Triumph"]

    def test_triumph(self):
        """Use Triumph"""
        self.plr.gain_card("Copper")
        self.plr.perform_event(self.event)
        self.assertIsNotNone(self.plr.discardpile["Estate"])
        scores = self.plr.get_score_details()
        self.assertEqual(scores["Triumph"], 2)
        self.assertEqual(self.plr.debt, 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
