#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Looting"""
import unittest
from dominion import Card, Game, Event, Piles


###############################################################################
class Event_Looting(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Gain a Loot"
        self.name = "Looting"
        self.cost = 6
        self.required_cards = ["Loot"]

    def special(self, game, player):
        """Gain a Loot"""
        player.gain_card("Loot")


###############################################################################
class TestLooting(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Looting"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Looting"]

    def test_with_treasure(self):
        """Use Looting"""
        self.plr.coins.add(6)
        self.plr.perform_event(self.card)
        found = any([True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
