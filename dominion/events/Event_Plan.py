#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Plan"""

import unittest

from dominion import Card, Game, Event, Token


###############################################################################
class Event_Plan(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your Trashing token to an Action Supply pile."
        self.name = "Plan"
        self.cost = 3

    def special(self, game, player):
        """Move your Trashing token to an Action Supply pile"""
        if stacks := player.card_pile_sel(
            num=1,
            prompt="What stack to add the Trashing Token to?",
            cardsrc=game.get_action_piles(),
        ):
            player.place_token(Token.TRASHING, stacks[0])


###############################################################################
class TestPlan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Plan"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Plan"]

    def test_play(self):
        """Perform a Plan"""
        self.plr.coins.add(3)
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens[Token.TRASHING], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
