#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Banquet(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Gain 2 Coppers and a non-Victory card costing up to 5"
        self.name = "Banquet"
        self.cost = 3

    def special(self, game, player):
        for _ in range(2):
            player.gain_card("Copper")
        player.plr_gain_card(
            5,
            types={
                Card.CardType.ACTION: True,
                Card.CardType.TREASURE: True,
                Card.CardType.VICTORY: False,
            },
        )


###############################################################################
class Test_Banquet(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Banquet"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Banquet"]

    def test_event(self):
        """Use the event"""
        self.plr.test_input = ["Get Silver"]
        self.plr.coins.add(3)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
