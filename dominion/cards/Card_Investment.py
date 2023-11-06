#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Investment"""

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Investment(Card.Card):
    """Investment"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """Trash a card from your hand.  Choose one: +$1;
            or trash this to reveal your hand for +1VP per differently named Treasure there."""
        self.name = "Investment"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.plr_trash_card(force=True)
        num_treas = len({_.name for _ in player.piles[Piles.HAND] if _.isTreasure()})
        if player.plr_choose_options(
            "Choose One? ",
            ("+1 Coin", True),
            (
                f"Trash this to reveal your hand for +1 VP per differently named Treasure there (currently {num_treas})",
                False,
            ),
        ):
            player.coins.add(1)
            return
        player.trash_card(self)
        player.output(f"Gaining {num_treas} victory points")
        player.add_score("Investment", num_treas)


###############################################################################
class TestInvestment(unittest.TestCase):
    """Test Investment"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Investment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Investment")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)

    def test_dont_trash(self) -> None:
        """Play but don't trash"""
        cash = self.plr.coins.get()
        self.plr.test_input = ["Trash Copper", "Coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cash + 1)

    def test_trash(self) -> None:
        """Play and trash"""
        cash = self.plr.coins.get()
        score = self.plr.get_score()
        self.plr.test_input = ["Trash Copper", "Trash this"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cash)
        self.assertIn("Investment", self.g.trash_pile)
        self.assertEqual(self.plr.get_score(), score + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
