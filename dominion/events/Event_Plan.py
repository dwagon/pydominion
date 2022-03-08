#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Plan(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Move your Trashing token to an Action Supply pile"
        self.name = "Plan"
        self.cost = 3

    def special(self, game, player):
        """Move your Trashing token to an Action Supply pile"""
        actionpiles = game.getActionPiles()
        stacks = player.cardSel(
            num=1,
            prompt="What stack to add the Trashing Token to?",
            cardsrc=actionpiles,
        )
        if stacks:
            player.place_token("Trashing", stacks[0].name)


###############################################################################
class Test_Plan(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=["Plan"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Plan"]

    def test_play(self):
        """Perform a Plan"""
        self.plr.addCoin(3)
        self.plr.test_input = ["Moat"]
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.tokens["Trashing"], "Moat")
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
