#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Sibyl(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_AUGUR,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 6
        self.name = "Sibyl"
        self.cards = 4
        self.actions = 1
        self.desc = """+4 Cards; +1 Action;
            Put a card from your hand on top of your deck, and another on the bottom."""

    def special(self, game, player):
        pass


###############################################################################
class Test_Sibyl(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Augurs"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Sibyl":
                break
        self.card = card

    def test_play(self):
        """Play a lich"""
        hndsz = self.plr.hand.size()
        self.plr.add_card(self.card, "hand")
        self.plr.set_discard("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), hndsz + 6)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_trash(self):
        """Trash the lich"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Silver"]
        self.g.set_trash("Silver")
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertIsNone(self.g.in_trash("Sibyl"))
        self.assertIsNone(self.g.in_trash("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Sibyl"))
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
