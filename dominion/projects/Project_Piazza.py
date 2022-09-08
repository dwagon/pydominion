#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_Piazza(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your turn, reveal the top card of your deck. If it's an Action, play it."
        self.name = "Piazza"
        self.cost = 5

    def hook_start_turn(self, game, player):
        c = player.next_card()
        if c.isAction():
            player.output("Piazza playing {}".format(c.name))
            player.add_card(c, "hand")
            player.play_card(c)
        else:
            player.output("Piazza revealed {} but it isn't an action - putting back".format(c.name))
            player.add_card(c, "topdeck")


###############################################################################
class Test_Piazza(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Piazza"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.deck.set("Copper", "Copper", "Copper", "Copper", "Copper", "Moat")
        self.plr.assign_project("Piazza")
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.played)
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_noaction(self):
        self.plr.deck.set("Province", "Silver")
        self.plr.assign_project("Piazza")
        self.plr.start_turn()
        self.assertEqual(self.plr.deck[-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
