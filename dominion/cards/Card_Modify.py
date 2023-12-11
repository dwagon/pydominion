#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Modify(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Modify"
        self.desc = """Trash a card from your hand. Choose one: +1 Card and +1 Action;
            or gain a card costing up to $2 more than the trashed card."""
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        tc = player.plr_trash_card(force=True)
        if tc is None:  # pragma: no coverage
            return
        cost = tc[0].cost + 2
        choice = player.plr_choose_options(
            "Pick one?",
            ("+1 Card and +1 Action", "card"),
            (f"Gain a card costing up to {cost}", "gain"),
        )
        if choice == "card":
            player.pickup_cards(1)
            player.add_actions(1)
        elif choice == "gain":
            player.plr_gain_card(cost=cost)


###############################################################################
class TestModify(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Modify"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Modify")

    def test_play_action(self) -> None:
        """Play the card gaining action"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash estate", "action"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)
        self.assertIn("Estate", self.g.trash_pile)

    def test_play_gain(self) -> None:
        """Play the card gaining a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash estate", "gain", "get silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
