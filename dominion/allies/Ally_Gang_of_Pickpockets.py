#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Gang_of_Pickpockets"""

import unittest
from dominion import Card, Game, Ally


###############################################################################
class Ally_Gang_Pickpockets(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, discard down to 4 cards in hand unless you spend a Favor."""
        self.name = "Gang of Pickpockets"

    def hook_start_turn(self, game, player):
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
class Test_Gang_Pickpockets(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, ally="Gang of Pickpockets", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spend_favor(self):
        """Spend a favor"""
        self.plr.favors.set(1)
        self.plr.test_input = ["Spend"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.favors.get(), 0)

    def test_discard(self):
        """Discard"""
        self.plr.hand.set("Estate", "Duchy", "Silver", "Gold", "Copper")
        self.plr.favors.set(1)
        self.plr.test_input = ["Discard", "Discard Duchy"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertEqual(self.plr.favors.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
