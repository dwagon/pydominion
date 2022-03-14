#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Conquest(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "Gain 2 Silvers. +1 VP per Silver you've gained this turn."
        self.name = "Conquest"
        self.cost = 6

    def special(self, game, player):
        for _ in range(2):
            player.gain_card("Silver")
        sc = 0
        for card in player.stats["gained"]:
            if card.name == "Silver":
                sc += 1
        player.output("Gained %d VP from Conquest" % sc)
        player.add_score("Conquest", sc)


###############################################################################
class Test_Conquest(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Conquest"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Conquest"]

    def test_event(self):
        """Use Conquest"""
        self.plr.addCoin(6)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertEqual(self.plr.get_score_details()["Conquest"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
