#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Conquest(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "Gain 2 Silvers. +1 VP per Silver you've gained this turn."
        self.name = "Conquest"
        self.cost = 6

    def special(self, game, player):
        for _ in range(2):
            player.gain_card("Silver")
        sc = 0
        for card in player.stats["gained"]:
            if card.name == "Silver":
                sc += 1
        player.output("Gained %d VP from Conquest" % sc)
        player.add_score("Conquest", sc)


###############################################################################
class Test_Conquest(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Conquest"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Conquest"]

    def test_event(self):
        """Use Conquest"""
        self.plr.coins.add(6)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.discardpile["Silver"])
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertEqual(self.plr.get_score_details()["Conquest"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
