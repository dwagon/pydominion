#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tanuki"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Tanuki(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SHADOW]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Trash a card from your hand. Gain a card costing up to $2 more than it."""
        self.name = "Tanuki"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. Gain a card costing up to $2 more than it."""
        if tc := player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain another costing up to 2 more than the one you trashed",
        ):
            cost = tc[0].cost
            player.plr_gain_card(cost + 2)


###############################################################################
class Test_Tanuki(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Tanuki"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tanuki")

    def test_nothing(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_trash_gain_nothing(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)

    def test_trash_gain_something(self) -> None:
        trash_size = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1", "1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
