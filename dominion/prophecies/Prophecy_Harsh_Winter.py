#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Harsh_Winter"""
import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Phase


###############################################################################
class Prophecy_Harsh_Winter(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """When you gain a card on your turn, if there's debt on its pile, take it;
                        otherwise put 2 debt on its pile."""
        self.name = "Harsh Winter"
        self.winter_cardpiles: dict[str, bool] = {}

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if self.winter_cardpiles.get(card.name, False):
            player.debt.add(2)
            player.output("Gained 2 debt from Harsh Winter")
            self.winter_cardpiles[card.name] = False
        else:
            self.winter_cardpiles[card.name] = True
        return {}

    def hook_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> str:
        if player.phase == Phase.BUY and self.winter_cardpiles.get(card.name, False):
            return "[+2 Debt]"
        return ""


###############################################################################
class Test_Harsh_Winter(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Harsh Winter"], initcards=["Mountain Shrine", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.test_input = ["Get Moat", "Get Mountain Shrine"]
        self.g.reveal_prophecy()
        self.plr.phase = Phase.BUY
        debt = self.plr.debt.get()
        self.assertEqual(self.g.get_card_from_pile("Copper").description(self.plr), "+1 coin")
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.debt.get(), debt)
        self.assertEqual(self.g.get_card_from_pile("Copper").description(self.plr), "+1 coin [+2 Debt]")
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.debt.get(), debt + 2)
        self.assertEqual(self.g.get_card_from_pile("Copper").description(self.plr), "+1 coin")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
