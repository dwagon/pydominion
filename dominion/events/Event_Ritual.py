#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Ritual(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "Gain a Curse. If you do, trash a card from your hand. +1VP per Coin it cost."
        self.name = "Ritual"
        self.cost = 4
        self.required_cards = ["Curse"]

    def special(self, game, player):
        card = player.gain_card("Curse")
        if card:
            tc = player.plr_trash_card(prompt="Trash a card, +1 VP per coin it costs")
            if tc:
                player.add_score("Ritual", tc[0].cost)


###############################################################################
class Test_Ritual(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Ritual"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Ritual"]

    def test_ritual(self):
        """Use Ritual"""
        self.plr.add_coins(4)
        self.plr.set_hand("Gold")
        self.plr.test_input = ["Gold"]
        self.plr.performEvent(self.event)
        self.assertEqual(self.plr.get_score_details()["Ritual"], 6)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertIsNotNone(self.plr.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
