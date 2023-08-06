#!/usr/bin/env python

import unittest
from dominion import Card, Game, Project


###############################################################################
class Project_StarChart(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you shuffle, you may pick one of the cards to go on top."
        self.name = "Star Chart"
        self.cost = 3

    def hook_pre_shuffle(self, game, player):
        names = {_.name for _ in player.discardpile}
        choices = []
        for name in names:
            choices.append(("Put {} on top".format(name), name))
        opt = player.plr_choose_options(
            "Pick a card to put on top of your deck", *choices
        )
        card = player.discardpile[opt]
        player.move_card(card, "topdeck")


###############################################################################
class Test_StarChart(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Star Chart"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project("Star Chart")
        self.plr.discardpile.set("Copper", "Copper", "Silver", "Gold", "Estate", "Gold")
        self.plr.deck.set()
        self.plr.test_input = ["Put Gold"]
        c = self.plr.next_card()
        self.g.print_state()
        self.assertEqual(c.name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
