#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Trade(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = (
            "Trash up to 2 cards from your hand (not played); Gain a silver per trashed"
        )
        self.name = "Trade"
        self.cost = 5

    def special(self, game, player):
        """Trash up to 2 cards from your hand. Gain a Silver per card you trashed"""
        trash = player.plr_trash_card(num=2)
        for _ in trash:
            player.gain_card("Silver")


###############################################################################
class Test_Trade(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Trade"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Trade"]

    def test_play(self):
        """Perform a Trade"""
        self.plr.add_coins(5)
        self.plr.set_hand("Copper", "Estate", "Gold")
        self.plr.test_input = ["copper", "estate", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, "Silver")
        self.assertIsNone(self.plr.in_hand("Copper"))
        self.assertIsNone(self.plr.in_hand("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
