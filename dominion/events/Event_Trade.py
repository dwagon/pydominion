#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event, NoCardException


###############################################################################
class Event_Trade(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Trash up to 2 cards from your hand (not played); Gain a silver per trashed"
        self.name = "Trade"
        self.cost = 5

    def special(self, game, player):
        """Trash up to 2 cards from your hand. Gain a Silver per card you trashed"""
        trash = player.plr_trash_card(num=2)
        if not trash:
            return
        for _ in trash:
            try:
                player.gain_card("Silver")
            except NoCardException:  # pragma: no coverage
                player.output("Not more Silver")


###############################################################################
class Test_Trade(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Trade"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Trade"]

    def test_play(self):
        """Perform a Trade"""
        self.plr.coins.add(5)
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Gold")
        self.plr.test_input = ["copper", "estate", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Silver")
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertNotIn("Estate", self.plr.piles[Piles.HAND])

    def test_trash_nothing(self):
        """Trash nothing"""
        self.plr.coins.add(5)
        self.plr.piles[Piles.HAND].set()
        self.plr.test_input = ["finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
