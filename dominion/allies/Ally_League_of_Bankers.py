#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/League_of_Bankers"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_League_Bankers(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your Buy phase, +$1 per 4 Favors you have (round down).  """
        self.name = "League of Bankers"

    def hook_pre_buy(self, game, player):
        cash = int(player.get_favors() / 4)
        player.output(f"League of Bankers gives you {cash} coin")
        player.add_coins(cash)


###############################################################################
class Test_League_Bankers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="League of Bankers", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.set_favors(5)
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.get_coins(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
