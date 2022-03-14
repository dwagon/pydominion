#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_RoadNetwork(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "When another player gains a Victory card, +1 Card."
        self.name = "Road Network"
        self.cost = 5

    def hook_allplayers_gain_card(self, game, player, owner, card):
        if card.isVictory() and owner != player:
            owner.pickup_cards(1)
            owner.output(
                "Road Network gives card due to {} picking up {}".format(
                    player.name, card.name
                )
            )


###############################################################################
class Test_RoadNetwork(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=2,
            initprojects=["Road Network"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr, self.other = self.g.player_list()

    def test_victory(self):
        self.plr.assign_project("Road Network")
        self.plr.set_deck("Gold")
        self.other.gain_card("Duchy")
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertIsNotNone(self.plr.in_hand("Gold"))

    def test_not_victory(self):
        self.plr.assign_project("Road Network")
        self.plr.set_deck("Gold")
        self.other.gain_card("Copper")
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertIsNone(self.plr.in_hand("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
