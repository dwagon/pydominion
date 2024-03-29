#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Crucible"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Crucible(Card.Card):
    """Crucible"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Trash a card from your hand. +$1 per $1 it costs."""
        self.name = "Crucible"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if cards := player.plr_trash_card(force=True):
            player.output(f"Gained {cards[0].cost} coin")
            player.coins.add(cards[0].cost)


###############################################################################
class TestCrucible(unittest.TestCase):
    """Test Crucible"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Crucible"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Crucible")

    def test_play(self) -> None:
        """Play a salvage"""
        self.plr.piles[Piles.HAND].set("Duchy", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
