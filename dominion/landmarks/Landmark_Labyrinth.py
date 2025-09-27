#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Labyrinth"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, Player, OptionKeys

LABYRINTH = "labyrinth"


###############################################################################
class Landmark_Labyrinth(Landmark.Landmark):
    """Labyrinth"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Labyrinth"

    def dynamic_description(self, player: Player.Player) -> str:
        return f"""When you gain a 2nd card in one of your turns,
                take 2VP from here ({player.game.specials[LABYRINTH]} left)"""

    def setup(self, game: Game.Game) -> None:
        game.specials[LABYRINTH] = 6 * game.numplayers

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if len(player.stats["gained"]) == 1:  # not including the current one
            player.add_score("Labyrinth", 2)
            player.output("Gained 2VP from Labyrinth")
            game.specials[LABYRINTH] -= 2
        return {}


###############################################################################
class Test_Labyrinth(unittest.TestCase):
    """Test Labyrinth"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Labyrinth"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Use Labyrinth"""
        self.assertNotIn("Labyrinth", self.plr.get_score_details())
        self.plr.gain_card("Copper")
        self.assertNotIn("Labyrinth", self.plr.get_score_details())
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.get_score_details()["Labyrinth"], 2)
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.get_score_details()["Labyrinth"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
