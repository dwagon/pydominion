#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event, NoCardException


###############################################################################
class Event_Ritual(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "Gain a Curse. If you do, trash a card from your hand. +1VP per Coin it cost."
        self.name = "Ritual"
        self.cost = 4
        self.required_cards = ["Curse"]

    def special(self, game, player):
        try:
            if card := player.gain_card("Curse"):
                tc = player.plr_trash_card(prompt="Trash a card, +1 VP per coin it costs")
                if tc:
                    player.add_score("Ritual", tc[0].cost)
        except NoCardException:
            player.output("No more Curses")


###############################################################################
class Test_Ritual(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Ritual"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Ritual"]

    def test_ritual(self):
        """Use Ritual"""
        self.plr.coins.add(4)
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.test_input = ["Gold"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.get_score_details()["Ritual"], 6)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Curse"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
