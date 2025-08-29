#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Gang_of_Pickpockets"""

import unittest

from dominion import Card, Game, Piles, Ally, Player


###############################################################################
class Ally_Gang_Pickpockets(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, discard down to 4 cards in hand unless you spend a Favor."""
        self.name = "Gang of Pickpockets"

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if not player.favors.get():
            player.plr_discard_down_to(4)
            return
        choice = player.plr_choose_options(
            "Spend a favor or discard down to 4",
            ("Spend favor", True),
            ("Discard down to 4", False),
        )
        if choice:
            player.favors.add(-1)
        else:
            player.plr_discard_down_to(4)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if kind == "choices":
        return False
    num_to_discard = len(player.piles[Piles.HAND]) - 4
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Gang_Pickpockets(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, allies="Gang of Pickpockets", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_spend_favor(self) -> None:
        """Spend a favor"""
        self.plr.favors.set(1)
        self.plr.test_input = ["Spend"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.favors.get(), 0)

    def test_discard(self) -> None:
        """Discard"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Silver", "Gold", "Copper")
        self.plr.favors.set(1)
        self.plr.test_input = ["Discard", "Discard Duchy"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        self.assertEqual(self.plr.favors.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
