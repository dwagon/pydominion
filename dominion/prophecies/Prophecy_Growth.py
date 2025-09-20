#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles


###############################################################################
class Prophecy_Growth(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "When you gain a Treasure, gain a cheaper card."
        self.name = "Growth"

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.isTreasure():
            player.output("Gain a card from Growth")
            cheaper = card.cost - 1
            player.plr_gain_card(cheaper, force=True)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None) -> list["Card.Card"]:  # pragma: no cover
    """If we need to pick up cards - pick up the best"""
    picked = []
    for card in kwargs["cardsrc"]:
        if card.name == "Province":
            picked.append((6, card))
        elif card.name == "Gold":
            picked.append((5, card))
        elif card.name == "Duchy":
            picked.append((4, card))
        elif card.name == "Silver":
            picked.append((3, card))
        elif card.name == "Estate":
            picked.append((2, card))
        elif card.name == "Copper":
            picked.append((1, card))
    picked.sort()
    return [picked[-1][1]]


###############################################################################
class Test_Growth(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Growth"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.test_input = ["Get Duchy"]
        self.plr.gain_card("Gold")
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
