#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Salvager"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Salvager(Card.Card):
    """Salvager"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = (
            """+1 Buy. Trash a card from your hand. Gain Coins equal to its cost."""
        )
        self.name = "Salvager"
        self.buys = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if card := player.plr_trash_card(force=True):
            player.output(f"Gained {card[0].cost} coin")
            player.coins.add(card[0].cost)


###############################################################################
class TestSalvager(unittest.TestCase):
    """Test Salvager"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Salvager"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Salvager")

    def test_play(self) -> None:
        """Play a salvage"""
        self.plr.piles[Piles.HAND].set("Duchy", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
