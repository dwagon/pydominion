#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Sprawling_Castle"""
import unittest
from typing import Optional

from dominion import Game, Card, Piles, Player, OptionKeys, NoCardException
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_SprawlingCastle(CastleCard):
    """Sprawling Castle"""

    def __init__(self) -> None:
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 8
        self.desc = """4VP. When you gain this, gain a Duchy or 3 Estates."""
        self.victory = 4
        self.name = "Sprawling Castle"
        self.pile = "Castles"

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        if player.plr_choose_options(
            "Gain a Duchy or 3 Estates",
            ("Gain a Duchy", True),
            ("Gain 3 Estates", False),
        ):
            player.gain_card("Duchy")
        else:
            for _ in range(3):
                try:
                    player.gain_card("Estate")
                except NoCardException:  # pragma: no coverage
                    player.output("No more Estates")
                    break
        return {}


###############################################################################
class TestSprawlingCastle(unittest.TestCase):
    """Test Sprawling Castle"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Castles"], badcards=["Duchess"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card: Optional[Card.Card] = None

    def test_play(self) -> None:
        """Play a sprawling castle"""
        while True:
            self.card = self.g.get_card_from_pile("Castles")
            if self.card.name == "Sprawling Castle":
                break
        self.plr.add_card(self.card, Piles.HAND)
        self.assertEqual(self.plr.get_score_details()["Sprawling Castle"], 4)

    def test_gain_duchy(self) -> None:
        """Gain duchy through Sprawling Castle"""
        while True:
            self.card = self.g.get_card_from_pile("Castles")
            if self.card.name == "Opulent Castle":  # One before Sprawling
                break
        self.plr.test_input = ["duchy"]
        self.plr.gain_card("Castles")
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1 + 1)

    def test_gain_estate(self) -> None:
        """Gain estates through Sprawling Castle"""
        while True:
            self.card = self.g.get_card_from_pile("Castles")
            if self.card.name == "Opulent Castle":  # One before Sprawling
                break
        self.plr.test_input = ["estates"]
        self.plr.gain_card("Castles")
        self.assertNotIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.g.print_state()
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
