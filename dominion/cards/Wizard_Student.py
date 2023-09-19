#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Student(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.WIZARD,  # pylint: disable=no-member
            Card.CardType.LIAISON,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.name = "Student"
        self.actions = 1
        self.pile = "Wizards"
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
        trashed = player.plr_trash_card(
            prompt="Pick a card to trash", num=1, force=True
        )
        if trashed and trashed[0].isTreasure():
            player.favors.add(1)
            player.piles[Piles.PLAYED].remove(self)
            player.add_card(self, "deck")


###############################################################################
class TestStudent(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_trash_treas(self):
        """Play a student - don't rotate, but trash treasure"""
        card = self.g.get_card_from_pile("Wizards", "Student")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Don't change", "Trash Copper"]
        favors = self.plr.favors.get()
        self.plr.play_card(card)
        self.assertIn("Copper", self.g.trashpile)
        self.assertIn("Student", self.plr.piles[Piles.DECK])
        self.assertEqual(self.plr.favors.get(), favors + 1)

    def test_play_trash_non_treas(self):
        """Play a student - don't rotate, but trash a non treasure"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Student":
                break
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Don't change", "Trash Estate"]
        favors = self.plr.favors.get()
        self.plr.play_card(card)
        self.assertIn("Estate", self.g.trashpile)
        self.assertNotIn("Student", self.plr.piles[Piles.DECK])
        self.assertEqual(self.plr.favors.get(), favors)

    def test_play_trash_rotate(self):
        """Play a student - rotate, and trash a non treasure"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Student":
                break
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Rotate", "Trash Estate"]
        self.plr.play_card(card)
        card = self.g["Wizards"].remove()
        self.assertEqual(card.name, "Conjurer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
