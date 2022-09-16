#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Desperation(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Once per turn: You may gain a Curse. If you do, +1 Buy and +2 Coin."
        self.name = "Desperation"
        self.cost = 0
        self.required_cards = ["Curse"]

    def special(self, game, player):
        opt = player.plr_choose_options(
            "Gain a curse to get +1 Buy and +2 Coin",
            ("Nope", False),
            ("Gain a curse", True),
        )
        if opt:
            if player.do_once("Desperation"):
                curse = player.gain_card("Curse")
                if curse:
                    player.buys.add(1)
                    player.coins.add(2)
                else:
                    player.output("Didn't get a Curse so no benefits")
            else:
                player.output("You've already done Desperation this turn")


###############################################################################
class Test_Desperation(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            eventcards=["Desperation"],
            initcards=["Cellar", "Chapel", "Moat", "Militia", "Village", "Workshop"],
            badcards=["Hostelry", "Border Village", "Inn", "Cursed Village"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Desperation"]

    def test_Desperation(self):
        """Use Desperation"""
        self.plr.coins.add(0)
        self.plr.test_input = ["Gain a curse"]
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.discardpile["Curse"])
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
