#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Change"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Change(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """If you have any Debt, +$3.
            Otherwise, trash a card from your hand, and gain a card costing more $ than it.
            Debt equal to the difference in $."""
        self.name = "Change"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """If you have any Debt, +$3.
        Otherwise, trash a card from your hand, and gain a card costing more $ than it.
        Debt equal to the difference in $."""
        if player.debt:
            player.coins.add(3)
            return
        if cards := player.plr_trash_card():
            card = cards[0]
            if new_card := player.plr_gain_card(cost=card.cost, modifier="greater"):
                player.debt.add(new_card.cost - card.cost)


###############################################################################
class TestChange(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Change"], badcards=["Gold Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Change")

    def test_play_debt(self) -> None:
        """Play a Change with debt"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.debt.set(3)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_play_no_debt(self) -> None:
        """Play a Change with no debt"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.debt.set(0)
        self.plr.test_input = ["Trash Copper", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.debt.get(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
