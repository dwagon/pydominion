#!/usr/bin/env python

import unittest
from dominion import Game, Card
from dominion.cards.Card_Wizards import WizardCard


###############################################################################
class Card_Conjurer(WizardCard):
    def __init__(self):
        WizardCard.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_WIZARD, Card.TYPE_DURATION]
        self.base = Game.ALLIES
        self.cost = 4
        self.name = "Conjurer"
        self.desc = """TBA"""


###############################################################################
class Test_Conjurer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        """Play a sprawling castle"""
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Grand Castle":
                break
        self.plr.add_card(self.card, "hand")
        self.assertEqual(self.plr.get_score_details()["Grand Castle"], 5)

    def test_gain(self):
        """Gain Grand Castle"""
        self.plr.set_hand("Duchy", "Province")
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Sprawling Castle":  # One before Grand
                break
        self.plr.gain_card("Castles")
        self.assertEqual(self.plr.get_score_details()["Grand Castle"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
