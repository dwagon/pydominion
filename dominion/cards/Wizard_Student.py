#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Student(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_WIZARD,  # pylint: disable=no-member
            Card.TYPE_LIAISON,
        ]
        self.base = Game.ALLIES
        self.cost = 3
        self.name = "Student"
        self.actions = 1
        self.desc = """+1 Action;
            You may rotate the Wizards;
            Trash a card from your hand. If it's a Treasure, +1 Favor and put this onto your deck."""

    def special(self, game, player):
        opt = player.plr_choose_options(
            "Do you want to rotate the Wizards?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game["Wizards"].rotate()
        trshd = player.plr_trash_card(prompt="Pick a card to trash", num=1, force=True)
        if trshd[0].isTreasure():
            player.add_favors(1)
            player.played.remove(self)
            player.add_card(self, "deck")


###############################################################################
class Test_Student(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_trash_treas(self):
        """Play a student - don't rotate, but trash treasure"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Student":
                break
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Don't change", "Trash Copper"]
        favs = self.plr.get_favors()
        self.plr.play_card(card)
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIn("Student", self.plr.deck)
        self.assertEqual(self.plr.get_favors(), favs + 1)

    def test_play_trash_non_treas(self):
        """Play a student - don't rotate, but trash a non treasure"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Student":
                break
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Don't change", "Trash Estate"]
        favs = self.plr.get_favors()
        self.plr.play_card(card)
        self.assertIsNotNone(self.g.in_trash("Estate"))
        self.assertNotIn("Student", self.plr.deck)
        self.assertEqual(self.plr.get_favors(), favs)

    def test_play_trash_rotate(self):
        """Play a student - rotate, and trash a non treasure"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Student":
                break
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Rotate", "Trash Estate"]
        self.plr.play_card(card)
        card = self.g["Wizards"].remove()
        self.assertEqual(card.name, "Conjurer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
