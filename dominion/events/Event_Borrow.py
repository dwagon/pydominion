#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Borrow(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Once per turn - place -1 Card token and gain 1 Coin"
        self.name = "Borrow"
        self.cost = 0

    def special(self, game, player):
        """Once per turn: If your -1 Card Token isn't on your deck put it
        there and +1 Coin"""
        if not player.do_once("Borrow"):
            player.output("Already used Borrow this turn")
            return
        if player.card_token:
            player.output("-1 Card token already in play")
            return
        player.card_token = True
        player.coins.add(1)


###############################################################################
class Test_Borrow(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Borrow"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Borrow"]

    def test_play(self):
        """Perform a Borrow"""
        self.plr.coin = 0
        self.plr.perform_event(self.card)
        self.assertTrue(self.plr.card_token)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_play_alreadyset(self):
        """Perform a Borrow"""
        self.plr.card_token = True
        self.plr.coin = 0
        self.plr.perform_event(self.card)
        self.assertTrue(self.plr.card_token)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
