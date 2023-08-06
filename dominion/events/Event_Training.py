#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Training(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your +1 Coin Token to an Action Supply Pile"
        self.name = "Training"
        self.cost = 6

    def special(self, game, player):
        """Move your +1 Coin token to an Action Supply Pile"""
        actionpiles = game.getActionPiles()
        stacks = player.card_sel(num=1, prompt="What stack to add the +1 Coin Token to?", cardsrc=actionpiles)
        if stacks:
            player.place_token("+1 Coin", stacks[0].name)


###############################################################################
class Test_Training(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Training"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Training"]

    def test_with_treasure(self):
        """Use Training"""
        self.plr.coins.add(6)
        self.plr.test_input = ["moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens["+1 Coin"], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
