#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Bureaucracy"""
import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles


###############################################################################
class Prophecy_Bureaucracy(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "When you gain a card that doesn't cost $0, gain a Copper."
        self.name = "Bureaucracy"

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.cost != 0 or card.debtcost:
            player.output(f"Gaining a Copper from Bureaucracy")
            player.gain_card("Copper")
        return {}


###############################################################################
class Test_Bureaucracy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Bureaucracy"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active - gaining expensive"""
        self.plr.gain_card("Gold")
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])

    def test_play_cheap(self) -> None:
        """Play when prophecy active - gaining cheap"""
        self.plr.gain_card("Copper")
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
