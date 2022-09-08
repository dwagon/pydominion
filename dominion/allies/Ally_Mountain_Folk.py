#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Mountain_Folk """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Mountain_Folk(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = "At the start of your turn, you may spend 5 Favors for +3 Cards."
        self.name = "Mountain Folk"

    def hook_start_turn(self, game, player):
        if player.get_favors() < 5:
            return
        opt = player.plr_choose_options(
            "Spend 5 favours for +3 cards?",
            ("Do not spend", False),
            ("Spend favors", True),
        )
        if opt:
            player.add_favors(-5)
            player.pickup_cards(3)


###############################################################################
class Test_Mountain_Folk(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Mountain Folk", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play and gain a card"""
        self.plr.set_favors(6)
        hndsz = self.plr.hand.size()
        self.plr.test_input = ["Spend favors"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_favors(), 1)
        self.assertEqual(self.plr.hand.size(), hndsz + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
