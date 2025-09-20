#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Student(Card.Card):
    def __init__(self) -> None:
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

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.plr_choose_options(
            "Do you want to rotate the Wizards?",
            ("Don't change", False),
            ("Rotate", True),
        ):
            game.card_piles["Wizards"].rotate()
        if trashed := player.plr_trash_card(prompt="Pick a card to trash", num=1, force=True):
            if trashed[0].isTreasure():
                player.favors.add(1)
                player.move_card(self, Piles.DECK)


###############################################################################
class TestStudent(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards", "Throne Room", "Golem"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_trash_treas(self) -> None:
        """Play a student - don't rotate, but trash treasure"""
        card = self.g.get_card_from_pile("Wizards", "Student")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Don't change", "Trash Copper"]
        favors = self.plr.favors.get()
        self.plr.play_card(card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Student", self.plr.piles[Piles.DECK])
        self.assertEqual(self.plr.favors.get(), favors + 1)

    def test_play_trash_non_treas(self) -> None:
        """Play a student - don't rotate, but trash a non treasure"""
        card = self.g.get_card_from_pile("Wizards", "Student")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Don't change", "Trash Estate"]
        favors = self.plr.favors.get()
        self.plr.play_card(card)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertNotIn("Student", self.plr.piles[Piles.DECK])
        self.assertEqual(self.plr.favors.get(), favors)

    def test_play_not_from_hand(self) -> None:
        """Play student via a golem, so it isn't in the hand when played"""
        self.g.get_card_from_pile("Wizards", "Student")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.piles[Piles.DECK].set("Copper", "Student")
        golem = self.g.get_card_from_pile("Golem")
        self.plr.test_input = ["Don't change", "Copper"]
        self.plr.play_card(golem)
        self.assertIn("Copper", self.g.trash_pile)

    def test_play_trash_rotate(self) -> None:
        """Play a student - rotate, and trash a non treasure"""
        card = self.g.get_card_from_pile("Wizards", "Student")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Rotate", "Trash Estate"]
        self.plr.play_card(card)
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(card.name, "Conjurer")

    def test_play_twice(self) -> None:
        """Play twice"""
        card = self.g.get_card_from_pile("Wizards", "Student")
        throne = self.g.get_card_from_pile("Throne Room")
        self.plr.piles[Piles.HAND].set("Silver", "Copper")
        self.plr.add_card(card, Piles.HAND)
        self.plr.add_card(throne, Piles.HAND)
        self.plr.test_input = [
            "Play Student",
            "Rotate",
            "Trash Silver",
            "Rotate",
            "Trash Copper",
        ]
        favors = self.plr.favors.get()
        self.plr.play_card(throne)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Silver", self.g.trash_pile)
        self.assertEqual(self.plr.favors.get(), favors + 2)
        self.assertEqual(card.location, Piles.DECK)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
