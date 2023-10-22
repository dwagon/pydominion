#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Piazza(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, reveal the top card of your deck. If it's an Action, play it."
        self.name = "Piazza"
        self.cost = 5

    def hook_start_turn(self, game, player):
        c = player.next_card()
        if c.isAction():
            player.output(f"Piazza playing {c.name}")
            player.add_card(c, Piles.HAND)
            player.play_card(c)
        else:
            player.output(
                f"Piazza revealed {c.name} but it isn't an action - putting back"
            )
            player.add_card(c, "topdeck")


###############################################################################
class TestPiazza(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, projects=["Piazza"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        self.plr.piles[Piles.DECK].set(
            "Copper", "Copper", "Copper", "Copper", "Copper", "Moat"
        )
        self.plr.assign_project("Piazza")
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_noaction(self):
        self.plr.piles[Piles.DECK].set("Province", "Silver")
        self.plr.assign_project("Piazza")
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
