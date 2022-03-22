#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Stampede(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = (
            "If you have 5 or fewer cards in play, gain 5 Horses onto your deck."
        )
        self.name = "Stampede"
        self.cost = 5
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        if player.played.size() <= 5:
            for _ in range(5):
                player.gain_card("Horse")
        else:
            player.output("You have played too many cards this turn")


###############################################################################
class Test_Stampede(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            eventcards=["Stampede"],
            initcards=["Cellar", "Chapel", "Moat", "Militia", "Village", "Workshop"],
            badcards=["Hostelry", "Border Village", "Inn", "Cursed Village"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Stampede"]

    def test_Stampede(self):
        """Use Stampede"""
        self.plr.add_coins(5)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.in_discard("Horse"))
        self.assertEqual(self.plr.discardpile.size(), 5)

    def test_no_Stampede(self):
        """Use Stampede with played lots"""
        self.plr.set_played("Copper", "Silver", "Gold", "Copper", "Silver", "Gold")
        self.plr.add_coins(5)
        self.plr.perform_event(self.card)
        self.assertIsNone(self.plr.in_discard("Horse"))
        self.assertEqual(self.plr.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
