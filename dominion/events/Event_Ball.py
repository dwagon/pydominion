#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Ball(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Take -1 Coin token; Gain 2 cards each costing up to 4 Coin"
        self.name = "Ball"
        self.cost = 5

    def special(self, game, player):
        player.coin_token = True
        for _ in range(2):
            player.plr_gain_card(cost=4)


###############################################################################
class Test_Ball(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Ball"], initcards=["Militia", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Ball"]

    def test_ball(self):
        """Use Ball"""
        self.plr.coins.add(5)
        self.plr.test_input = ["militia", "moat"]
        self.plr.perform_event(self.card)
        self.assertTrue(self.plr.coin_token)
        self.assertIsNotNone(self.plr.discardpile["Militia"])
        self.assertIsNotNone(self.plr.discardpile["Moat"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
