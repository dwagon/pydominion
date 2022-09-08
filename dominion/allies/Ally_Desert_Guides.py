#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Desert_Guides """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Desert_Guides(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your turn, you may spend a Favor to discard your hand and draw 5 cards. Repeat as desired."""
        self.name = "Desert Guides"

    def hook_start_turn(self, game, player):
        while True:
            if not player.get_favors():
                return
            choice = player.plr_choose_options(
                "Spend a favor to discard your hand and draw 5 cards? ",
                ("Do nothing", False),
                (f"Spend favor (You have {player.get_favors()} favors)", True),
            )
            if not choice:
                return
            player.discard_hand()
            player.pickup_cards(5)
            player.add_favors(-1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Desert_Guides(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Desert Guides", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_nothing(self):
        """Play but do nothing"""
        self.plr.set_favors(1)
        self.plr.test_input = ["Do nothing"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_favors(), 1)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.discardpile.size(), 0)

    def test_play_discard(self):
        """Play and discard hand"""
        self.plr.set_favors(1)
        self.plr.test_input = ["Spend favor"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_favors(), 0)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.discardpile.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
