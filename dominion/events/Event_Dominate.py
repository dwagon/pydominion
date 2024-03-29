#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Dominate(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "Gain a Province. If you do, +9VP."
        self.name = "Dominate"
        self.cost = 14

    def special(self, game, player):
        c = player.gain_card("Province")
        if c:
            player.add_score("Dominate", 9)


###############################################################################
class Test_Dominate(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Dominate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Dominate"]

    def test_play(self):
        """Perform a Dominate"""
        self.plr.coins.add(14)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Province"])
        self.assertEqual(self.plr.get_score_details()["Dominate"], 9)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
