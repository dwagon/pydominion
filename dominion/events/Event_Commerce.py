#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Commerce(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Gain a Gold per differently named card you've gained this turn."
        self.name = "Commerce"
        self.cost = 5

    def special(self, game, player):
        gains = {_.name for _ in player.stats["gained"]}
        for _ in gains:
            player.gain_card("Gold")


###############################################################################
class Test_Commerce(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, eventcards=["Commerce"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Commerce"]

    def test_Commerce(self):
        """Use Commerce"""
        self.plr.coins.add(5)
        self.plr.gain_card("Moat")
        self.plr.perform_event(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.plr.discardpile["Gold"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
