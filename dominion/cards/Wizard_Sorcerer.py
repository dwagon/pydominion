#!/usr/bin/env python

import unittest
from dominion import Game, Card
from dominion.cards.Card_Wizards import WizardCard


###############################################################################
class Card_Sorcerer(WizardCard):
    def __init__(self):
        WizardCard.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_WIZARD, Card.TYPE_ATTACK]
        self.base = Game.ALLIES
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.name = "Sorcerer"
        self.desc = """+1 Card; +1 Action; Each other player names a card,
            then reveals the top card of their deck. If wrong, they gain a Curse."""


###############################################################################
class Test_Sorcerer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Sorcerer":
                break
        self.plr.add_card(card, "hand")
        hndsz = self.plr.hand.size()
        self.plr.play_card(card)
        self.assertEqual(self.plr.hand.size(), hndsz)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
