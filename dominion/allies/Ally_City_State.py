#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/City-state """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player, OptionKeys


###############################################################################
class Ally_CityState(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When you gain an Action card during your turn, you may spend 2 Favors to play it."""
        self.name = "City State"

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if not card.isAction():
            return {}
        if player.favors.get() < 2:
            return {}
        if player.plr_choose_options(
            f"Play {card} from City State?",
            ("Do nothing", False),
            ("Play Card", True),
        ):
            player.play_card(card, discard=False, cost_action=False)
            player.favors.add(-2)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # type: ignore
    return []


###############################################################################
class TestCityState(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, allies="City State", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.HAND].set()
        self.plr.favors.set(2)
        self.plr.actions.set(0)
        self.plr.test_input = ["Play"]
        self.plr.gain_card("Underling")
        self.assertEqual(self.plr.favors.get(), 2 - 2 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)

    def test_dont_play(self) -> None:
        """Don't play card"""
        self.plr.piles[Piles.HAND].set()
        self.plr.favors.set(2)
        self.plr.actions.set(0)
        self.plr.test_input = ["nothing"]
        self.plr.gain_card("Underling")
        self.assertEqual(self.plr.favors.get(), 2)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
