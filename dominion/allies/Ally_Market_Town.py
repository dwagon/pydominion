#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Market_Towns """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player


###############################################################################
class Ally_Market_Towns(Ally.Ally):
    """Market Towns"""

    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your Buy phase, you may spend a Favor to
            play an Action card from your hand. Repeat as desired."""
        self.name = "Market Towns"

    def hook_pre_buy(self, game: Game.Game, player: Player.Player) -> None:
        while player.favors.get():
            # Suitable actions can change between invocations
            acts = [_ for _ in player.piles[Piles.HAND] if _.playable and _.isAction()]
            if not acts:
                break
            opts = [("Do Nothing", None)]
            for act in acts:
                opts.append((f"Play {act.name}", act))
            if chc := player.plr_choose_options(
                "Spend an favor to play an action?", *opts
            ):
                player.play_card(chc, cost_action=False)
                acts.remove(chc)
                player.favors.add(-1)
            else:
                break


###############################################################################
def botresponse(
    player: "Player.Player",
    kind: str,
    args: Any | None = None,
    kwargs: Any | None = None,
) -> Any:
    return None


###############################################################################
class TestMarketTowns(unittest.TestCase):
    """Test Market Towns"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, allies="Market Towns", initcards=["Underling", "Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play a Market Town"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Silver", "Gold")
        self.plr.favors.set(3)
        self.plr.test_input = ["Play Moat", "End Phase"]
        hand_size = self.plr.piles[Piles.HAND].size()
        self.plr.buy_phase()
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.favors.get(), 2)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), hand_size + 2 - 1
        )  # Moat - played


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
