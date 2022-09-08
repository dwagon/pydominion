#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Pathfinding(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Move your +1 Card Token to an Action Supply Pile"
        self.name = "Pathfinding"
        self.cost = 8

    def special(self, game, player):
        """Move your +1 Card token to an Action Supply Pile"""
        actionpiles = game.getActionPiles()
        stacks = player.card_sel(
            num=1, prompt="What stack to add the +1 Card Token to?", cardsrc=actionpiles
        )
        if stacks:
            player.place_token("+1 Card", stacks[0].name)


###############################################################################
class Test_Pathfinding(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Pathfinding"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Pathfinding"]

    def test_with_treasure(self):
        """Use Pathfinding"""
        self.plr.add_coins(8)
        self.plr.test_input = ["moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens["+1 Card"], "Moat")
        self.assertEqual(self.plr.get_coins(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
