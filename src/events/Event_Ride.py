#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Ride(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Gain a Horse."
        self.name = "Ride"
        self.cost = 2
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        player.gainCard("Horse")


###############################################################################
class Test_Ride(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            eventcards=["Ride"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Ride"]

    def test_Ride(self):
        """Use Ride"""
        self.plr.addCoin(2)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Horse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
