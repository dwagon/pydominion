#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Turtle"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Way, OptionKeys, Player


###############################################################################
class Way_Turtle(Way.Way):
    """Turtle"""

    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = (
            "Set this aside. If you did, play it at the start of your next turn."
        )
        self.name = "Way of the Turtle"

    def special_way(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        player.defer_card(card)
        return {OptionKeys.DISCARD: False}


###############################################################################
class TestTurtle(unittest.TestCase):
    """Test Turtle"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Turtle"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Turtle"]

    def test_play(self) -> None:
        """Perform a Turtle"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
