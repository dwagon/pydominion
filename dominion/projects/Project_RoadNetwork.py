#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_RoadNetwork(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When another player gains a Victory card, +1 Card."
        self.name = "Road Network"
        self.cost = 5

    def hook_allplayers_gain_card(self, game, player, owner, card):
        if card.isVictory() and owner != player:
            owner.pickup_cards(1)
            owner.output(
                f"Road Network gives card due to {player.name} picking up {card.name}"
            )


###############################################################################
class TestRoadNetwork(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initprojects=["Road Network"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr, self.other = self.g.player_list()

    def test_victory(self):
        self.plr.assign_project("Road Network")
        self.plr.piles[Piles.DECK].set("Gold")
        self.other.gain_card("Duchy")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_not_victory(self):
        self.plr.assign_project("Road Network")
        self.plr.piles[Piles.DECK].set("Gold")
        self.other.gain_card("Copper")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
