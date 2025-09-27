#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Battlefield"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, OptionKeys, Player

BATTLEFIELD = "battlefield"


###############################################################################
class Landmark_Battlefield(Landmark.Landmark):
    """Battlefield"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Battlefield"

    def dynamic_description(self, player: Player.Player) -> str:
        return f"When you gain a Victory card, take 2VP from here. ({player.game.specials[BATTLEFIELD]} left)"

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.isVictory() and game.specials[BATTLEFIELD] >= 0:
            game.specials[BATTLEFIELD] -= 2
            player.output("Gained 2VP from Battlefield")
            player.add_score("Battlefield", 2)
        return {}

    def setup(self, game: Game.Game) -> None:
        game.specials[BATTLEFIELD] = 6 * game.numplayers


###############################################################################
class TestBattlefield(unittest.TestCase):
    """Test Battlefield"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            landmarks=["Battlefield"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self) -> None:
        """Use Battlefield"""
        self.plr.coins.set(5)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Battlefield"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
