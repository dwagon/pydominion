#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Windfall(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "If your deck and discard pile are empty, gain 3 Golds"
        self.name = "Windfall"
        self.cost = 5

    def special(self, game, player):
        if player.piles[Piles.DECK].is_empty() and player.piles[Piles.DISCARD].is_empty():
            for _ in range(3):
                player.gain_card("Gold")


###############################################################################
class TestWindfall(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Windfall"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Windfall"]

    def test_play(self):
        """Perform a Windfall"""
        self.plr.coins.add(5)
        self.plr.piles[Piles.DISCARD].set()
        self.plr.piles[Piles.DECK].set()
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
        for card in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(card.name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
