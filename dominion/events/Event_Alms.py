#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Alms(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Alms"
        self.cost = 0

    def dynamic_description(self, player):
        if self.treasures(player):
            return "You have treasures in play so you can't gain a card costing up to 4"
        return "You have no treasures in play, gain a card costing up to 4"

    def treasures(self, player):
        t = 0
        t += sum([1 for c in player.piles[Piles.PLAYED] if c.isTreasure()])
        t += sum([1 for c in player.piles[Piles.HAND] if c.isTreasure()])
        return t

    def special(self, game, player):
        """Once per turn: If you have no treasures in play, gain a
        card costing up to 4"""
        if not player.do_once("Alms"):
            player.output("Already used Alms this turn")
            return

        if self.treasures(player) == 0:
            player.plr_gain_card(4)


###############################################################################
class Test_Alms(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Alms"], initcards=["Lurker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Alms"]

    def test_with_treasure(self):
        """Use Alms with treasures"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)

    def test_without_treasure(self):
        """Use Alms with no treasures"""
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.test_input = ["Lurker"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Lurker")

    def test_twice(self):
        """Use Alms twice"""
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.test_input = ["Lurker"]
        self.plr.perform_event(self.card)
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Lurker")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
