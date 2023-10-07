#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Demand"""

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Demand(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = (
            """ Gain a Horse and a card costing up to $4, both onto your deck."""
        )
        self.name = "Demand"
        self.required_cards = [("Card", "Horse")]
        self.cost = 5

    def special(self, game, player):
        player.gain_card("Horse", destination=Piles.DECK)
        player.plr_gain_card(cost=4, destination=Piles.DECK)


###############################################################################
class Test_Demand(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Demand"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Demand"]

    def test_with_treasure(self):
        """Use Demand"""
        self.plr.coins.set(5)
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Horse", self.plr.piles[Piles.DECK])
        self.assertIn("Moat", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
