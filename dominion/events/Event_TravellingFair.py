#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Travelling_Fair """

import unittest
from dominion import Game, Event


###############################################################################
class Event_TravellingFair(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = (
            "+2 Buys; When you gain a card this turn, you may put it onto your deck."
        )
        self.name = "Travelling Fair"
        self.cost = 2
        self.buys = 2

    def hook_gain_card(self, game, player, card):
        choice = player.plr_choose_options(
            "Do you want to put {} on the top of your deck?".format(card.name),
            ("Put {} on deck".format(card.name), "topdeck"),
            ("Discard {}".format(card.name), "discard"),
        )
        return {"destination": choice}


###############################################################################
class Test_TravellingFair(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Travelling Fair"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Travelling Fair"]

    def test_play_discard(self):
        """Perform a Travelling Fair"""
        self.plr.add_coins(2)
        self.plr.perform_event(self.card)
        self.plr.test_input = ["Discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNotNone(self.plr.discardpile["Gold"])
        self.assertNotIn("Gold", self.plr.deck)

    def test_play_deck(self):
        """Perform a Travelling Fair and deck the card"""
        self.plr.add_coins(2)
        self.plr.perform_event(self.card)
        self.plr.test_input = ["Put"]
        self.plr.gain_card("Gold")
        self.g.print_state()
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertNotIn("Gold", self.plr.discardpile)
        self.assertIn("Gold", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
