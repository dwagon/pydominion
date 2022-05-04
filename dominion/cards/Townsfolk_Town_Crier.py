#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Town_Crier(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_TOWNSFOLK,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 2
        self.name = "Town Crier"
        self.desc = """Choose one: +$2; or gain a Silver;
                or +1 Card and +1 Action.
                You may rotate the Townsfolk."""

    def special(self, game, player):
        opt = player.plr_choose_options(
            "Choose One: ",
            ("+$2", "cash"),
            ("Gain a Silver", "silver"),
            ("+1 Card and +1 action", "card"),
        )
        if opt == "cash":
            player.add_coins(2)
        elif opt == "silver":
            player.gain_card("Silver")
        elif opt == "card":
            player.pickup_card()
            player.add_actions(1)
        opt = player.plr_choose_options(
            "Do you want to rotate the Townsfolk?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game["Townsfolk"].rotate()


###############################################################################
class Test_Town_Crier(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g["Townsfolk"].remove()
            if self.card.name == "Town Crier":
                break
        self.plr.add_card(self.card, "hand")

    def test_play_rotate_cash(self):
        """Play a town crier - rotate, but get cash"""
        self.plr.test_input = ["+$2", "Rotate"]
        cns = self.plr.get_coins()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), cns + 2)
        card = self.g["Townsfolk"].remove()
        self.assertEqual(card.name, "Blacksmith")

    def test_play_retain_silver(self):
        """Play a town crier - don't rotate, but get silver"""
        self.plr.test_input = ["Silver", "Don't"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.discard["Silver"])
        card = self.g["Townsfolk"].remove()
        self.assertEqual(card.name, "Town Crier")

    def test_play_retain_card(self):
        """Play a town crier - don't rotate, but get card and action"""
        self.plr.test_input = ["card", "Don't"]
        hndsze = self.plr.hand.size()
        acts = self.plr.get_actions()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsze + 1 - 1)
        self.assertEqual(self.plr.get_actions(), acts + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
