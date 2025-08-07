#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Gather """

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Gather(Event.Event):
    """Gather"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "Gain a card costing exactly $3, a card costing exactly $4, and a card costing exactly $5."
        self.name = "Gather"
        self.cost = 7

    def special(self, game, player):
        player.plr_gain_card(3, modifier="equal")
        player.plr_gain_card(4, modifier="equal")
        player.plr_gain_card(5, modifier="equal")


###############################################################################
class Test_Gather(unittest.TestCase):
    """Test Gather"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Gather"], initcards=["Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Gather"]

    def test_play(self):
        """Perform a Gather"""
        self.plr.coins.add(7)
        self.plr.test_input=["Silver", "Militia", "Duchy"]
        self.plr.perform_event(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD] )
        self.assertIn("Militia", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
