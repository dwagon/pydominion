#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Fleet"""
import unittest

from dominion import Card, Game, Project, Player, Piles


###############################################################################
class Project_Fleet(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "After the game ends, there's an extra round of turns just for players with this."
        self.name = "Fleet"
        self.cost = 5

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        player.output("Fleet gives you another turn")
        player.turn()


###############################################################################
class Test_Fleet(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Fleet"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        self.plr.assign_project("Fleet")
        self.plr.test_input = ["End Phase", "Buy Copper", "End Phase"]
        self.plr.game_over()
        self.g.print_state()
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
        self.assertEqual(self.plr.actions.get(), 1)  # Should be reset to 1
        self.assertEqual(self.plr.buys.get(), 0)  # Had 1, bought a copper


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
