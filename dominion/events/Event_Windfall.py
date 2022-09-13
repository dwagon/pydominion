#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Windfall(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "If your deck and discard pile are empty, gain 3 Golds"
        self.name = "Windfall"
        self.cost = 5

    def special(self, game, player):
        if player.deck.is_empty() and player.discardpile.is_empty():
            for _ in range(3):
                player.gain_card("Gold")


###############################################################################
class Test_Windfall(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Windfall"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Windfall"]

    def test_play(self):
        """Perform a Windfall"""
        self.plr.coins.add(5)
        self.plr.discardpile.set()
        self.plr.deck.set()
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.discardpile.size(), 3)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
