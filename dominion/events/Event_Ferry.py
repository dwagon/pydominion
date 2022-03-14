#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Ferry(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Move your -2 Coin token to an Action Supply pile."
        self.name = "Ferry"
        self.cost = 3

    def special(self, game, player):
        actionpiles = game.getActionPiles()
        stacks = player.cardSel(
            num=1, prompt="What stack to add the -2 Coin Token to?", cardsrc=actionpiles
        )
        if stacks:
            player.place_token("-2 Cost", stacks[0].name)


###############################################################################
class Test_Ferry(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=["Ferry"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Ferry"]

    def test_play(self):
        self.plr.addCoin(3)
        self.plr.test_input = ["moat"]
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.tokens["-2 Cost"], "Moat")
        self.assertEqual(self.plr.get_coins(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
