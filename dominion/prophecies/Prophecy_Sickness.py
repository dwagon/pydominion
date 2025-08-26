#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Sickness"""

import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, Piles, NoCardException


###############################################################################
class Prophecy_Sickness(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "At the start of your turn, choose one: Gain a Curse onto your deck; or discard 3 cards."
        self.required_cards = ["Curse"]
        self.name = "Sickness"

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        option = player.plr_choose_options("Sickness", ("Gain a Curse", "curse"), ("Discard 3 cards", "discard"))
        if option == "curse":
            try:
                player.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")
        else:
            player.plr_discard_cards(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None) -> Any:  # pragma: no cover
    """"""
    return "curse"


###############################################################################
class Test_Sickness(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecy=["Sickness"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play_curse(self) -> None:
        """Play when prophecy active"""
        self.plr.test_input = ["Curse"]
        self.plr.start_turn()
        self.assertIn("Curse", self.plr.piles[Piles.DISCARD])

    def test_discard_cards(self) -> None:
        self.plr.test_input = ["Discard", "Copper", "Silver", "Estate", "Finish"]
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 3)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
