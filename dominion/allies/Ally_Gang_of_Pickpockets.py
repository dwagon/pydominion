#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Gang_of_Pickpockets"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Gang_Pickpockets(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your turn, discard down to 4 cards in hand unless you spend a Favor."""
        self.name = "Gang of Pickpockets"

    def hook_start_turn(self, game, player):
        if not player.get_favors():
            player.plr_discard_down_to(4)
            return
        choice = player.plr_choose_options(
            "Spend a favor or discard down to 4",
            ("Spend favor", True),
            ("Discard down to 4", False),
        )
        if choice:
            player.add_favors(-1)
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
        self.plr.set_favors(1)
        self.plr.test_input = ["Spend"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_favors(), 0)

    def test_discard(self):
        """Discard"""
        self.plr.set_hand("Estate", "Duchy", "Silver", "Gold", "Copper")
        self.plr.set_favors(1)
        self.plr.test_input = ["Discard", "Discard Duchy"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertEqual(self.plr.get_favors(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
