#!/usr/bin/env python

import unittest

from dominion import Card, Game, Event, Token


###############################################################################
class Event_Pathfinding(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your +1 Card Token to an Action Supply Pile"
        self.name = "Pathfinding"
        self.cost = 8

    def special(self, game, player):
        """Move your +1 Card token to an Action Supply Pile"""
        stacks = player.card_pile_sel(
            num=1,
            prompt="What stack to add the +1 Card Token to?",
            cardsrc=game.get_action_piles(),
        )
        if stacks:
            player.place_token(Token.PLUS_1_CARD, stacks[0])


###############################################################################
class TestPathfinding(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Pathfinding"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Pathfinding"]

    def test_with_treasure(self):
        """Use Pathfinding"""
        self.plr.coins.add(8)
        self.plr.test_input = ["moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens[Token.PLUS_1_CARD], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
