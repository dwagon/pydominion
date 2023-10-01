#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Desert_Guides """

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Desert_Guides(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, you may spend a Favor to discard your hand and draw 5 cards. Repeat as desired."""
        self.name = "Desert Guides"

    def hook_start_turn(self, game, player):
        while True:
            if not player.favors.get():
                return
            choice = player.plr_choose_options(
                "Spend a favor to discard your hand and draw 5 cards? ",
                ("Do nothing", False),
                (f"Spend favor (You have {player.favors.get()} favors)", True),
            )
            if not choice:
                return
            player.discard_hand()
            player.pickup_cards(5)
            player.favors.add(-1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Desert_Guides(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, allies="Desert Guides", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_nothing(self):
        """Play but do nothing"""
        self.plr.favors.set(1)
        self.plr.test_input = ["Do nothing"]
        self.plr.start_turn()
        self.assertEqual(self.plr.favors.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)

    def test_play_discard(self):
        """Play and discard hand"""
        self.plr.favors.set(1)
        self.plr.test_input = ["Spend favor"]
        self.plr.start_turn()
        self.assertEqual(self.plr.favors.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
