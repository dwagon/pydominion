#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Plan(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your Trashing token to an Action Supply pile"
        self.name = "Plan"
        self.cost = 3

    def special(self, game, player):
        """Move your Trashing token to an Action Supply pile"""
        actionpiles = game.getActionPiles()
        stacks = player.card_sel(
            num=1,
            prompt="What stack to add the Trashing Token to?",
            cardsrc=actionpiles,
        )
        if stacks:
            player.place_token("Trashing", stacks[0].name)


###############################################################################
class TestPlan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Plan"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Plan"]

    def test_play(self):
        """Perform a Plan"""
        self.plr.coins.add(3)
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens["Trashing"], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
