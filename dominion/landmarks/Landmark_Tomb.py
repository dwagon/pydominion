#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Piles, Landmark, Player, OptionKeys


###############################################################################
class Landmark_Tomb(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When you trash a card, +1VP"""
        self.name = "Tomb"

    def hook_trash_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        player.output("Gained 1 VP from Tomb")
        player.add_score("Tomb", 1)
        return {}


###############################################################################
class Test_Tomb(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Tomb"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_trash(self) -> None:
        """Test Tomb"""
        cu = self.plr.piles[Piles.HAND]["Copper"]
        self.plr.trash_card(cu)
        self.assertEqual(self.plr.get_score_details()["Tomb"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
