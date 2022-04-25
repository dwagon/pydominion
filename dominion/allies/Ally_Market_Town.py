#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Market_Towns """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Market_Towns(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = "At the start of your Buy phase, you may spend a Favor to play an Action card from your hand. Repeat as desired."
        self.name = "Market Towns"

    def hook_pre_buy(self, game, player):
        acts = [_ for _ in player.hand if _.playable and _.isAction()]
        while player.get_favors() and acts:
            opts = [("Do Nothing", None)]
            for act in acts:
                opts.append((f"Play {act.name}", act))
            chc = player.plr_choose_options("Spend an favor to play an action?", *opts)
            if chc:
                player.play_card(chc, costAction=False)
                acts.remove(chc)
                player.add_favors(-1)
            else:
                break


###############################################################################
class Test_Market_Towns(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, ally="Market Towns", initcards=["Underling", "Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play a Market Town"""
        self.plr.set_hand("Moat", "Copper", "Silver", "Gold")
        self.plr.set_favors(3)
        self.plr.test_input = ["Play Moat", "End Phase"]
        hndsz = self.plr.hand.size()
        self.plr.buy_phase()
        self.assertIsNotNone(self.plr.in_played("Moat"))
        self.assertIsNone(self.plr.in_hand("Moat"))
        self.assertEqual(self.plr.get_favors(), 2)
        self.assertEqual(self.plr.hand.size(), hndsz + 2 - 1)   # Moat - played


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
