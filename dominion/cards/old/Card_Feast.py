#!/usr/bin/env python

import unittest
from typing import Optional

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Feast(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash this card, Gain a card costing up to 5"
        self.name = "Feast"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash this card. Gain a card costing up to 5"""
        if self.trash_card(player):
            self.selectNewCard(game, player)

    def selectNewCard(self, game: Game.Game, player: Player.Player):
        player.output("Gain a card costing up to 5")
        choices: list[tuple[str, Optional[Card.Card]]] = [("Nothing", None)]
        for buyable in player.cards_under(5):
            choices.append((f"Get {buyable} ({buyable.cost} coin)", buyable))

        if card := player.plr_choose_options("What card do you wish?", *choices):
            player.gain_card(card.name)
            player.output(f"Took {card}")

    def trash_card(self, player):
        ans = player.plr_choose_options("Trash this card?", ("Keep this card", False), ("Trash this card", True))
        if ans:
            player.trash_card(self)
            return True
        return False


###############################################################################
class TestFeast(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Feast"],
            oldcards=True,
            badcards=["Den of Sin", "Ghost Town", "Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Feast")
        self.plr.add_card(self.card, Piles.HAND)

    def test_dontTrash(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["keep this"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize)
        try:
            self.assertEqual(self.plr.piles[Piles.PLAYED][0].name, "Feast")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trashForNothing(self):
        tsize = self.g.trash_pile.size()
        try:
            self.plr.test_input = ["trash", "nothing"]
            self.plr.play_card(self.card)
            self.assertEqual(self.g.trash_pile.size(), tsize + 1)
            self.assertIn("Feast", self.g.trash_pile)
            self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trashForSomething(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash", "Get Duchy"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trash_pile.size(), tsize + 1)
            self.assertIn("Feast", self.g.trash_pile)
            self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Duchy"])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
