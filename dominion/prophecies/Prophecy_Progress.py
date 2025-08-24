#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Progress"""
import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles


###############################################################################
class Prophecy_Progress(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "When you gain a card, put it onto your deck."
        self.name = "Progress"

    def hook_all_players_gain_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card.Card",
    ) -> dict[OptionKeys, Any]:
        return {OptionKeys.DESTINATION: Piles.TOPDECK}


###############################################################################
class Test_Progress(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Progress"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
