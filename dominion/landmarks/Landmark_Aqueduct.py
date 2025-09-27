#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Aqueduct"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, OptionKeys, Player

AQUEDUCT = "aqueduct"


###############################################################################
class Landmark_Aqueduct(Landmark.Landmark):
    """Aqueduct"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Aqueduct"
        self._goldvp = 8
        self._silvervp = 8
        self._vp = 0

    def dynamic_description(self, player: Player.Player) -> str:
        return f"""When you gain a Treasure, move 1 VP from its pile to this.
            When you gain a Victory card, take the VP from this.
            (Here: {player.game.specials[AQUEDUCT]['Aqueduct']} VP, Gold: {player.game.specials[AQUEDUCT]['Gold']} VP,
            Silver: {player.game.specials[AQUEDUCT]['Silver']} VP)"""

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """When you gain a Treasure, move 1VP from its pile to this.
        When you gain a Victory card, take the VP from this."""
        if game.specials[AQUEDUCT].get(card.name, 0):
            game.specials[AQUEDUCT][card.name] -= 1
            game.specials[AQUEDUCT]["Aqueduct"] += 1
            player.output(
                f"""{game.specials[AQUEDUCT][card.name]} VP left on {card.name};
                    {game.specials[AQUEDUCT]['Aqueduct']} VP on Aqueduct"""
            )
        if game.specials[AQUEDUCT]["Aqueduct"] and card.isVictory():
            player.output(f"Gained {game.specials[AQUEDUCT]['Aqueduct']} VP from Aqueduct")
            player.add_score("Aqueduct", game.specials[AQUEDUCT]["Aqueduct"])
            game.specials[AQUEDUCT]["Aqueduct"] = 0
        return {}

    def setup(self, game: "Game.Game") -> None:
        """Setup: Put 8VP on the Silver and Gold piles."""
        game.specials[AQUEDUCT] = {"Gold": 8, "Silver": 8, "Aqueduct": 0}


###############################################################################
class TestAqueduct(unittest.TestCase):
    """Test Aqueduct"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Aqueduct"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain_silver(self) -> None:
        """Use Aqueduct gaining Silver"""
        self.plr.buys.add(2)
        self.plr.coins.set(20)
        self.plr.buy_card("Silver")
        self.assertEqual(self.g.specials[AQUEDUCT]["Aqueduct"], 1)
        self.assertEqual(self.g.specials[AQUEDUCT]["Silver"], 7)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)

    def test_gain_gold(self) -> None:
        """Use Aqueduct gaining Gold"""
        self.plr.buys.add(2)
        self.plr.coins.set(20)
        self.plr.buy_card("Gold")
        self.assertEqual(self.g.specials[AQUEDUCT]["Aqueduct"], 1)
        self.assertEqual(self.g.specials[AQUEDUCT]["Gold"], 7)
        self.assertEqual(self.g.specials[AQUEDUCT]["Silver"], 8)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
