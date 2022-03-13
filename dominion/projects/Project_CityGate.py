#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_CityGate(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your turn, +1 Card, then put a card from your hand onto your deck."
        self.name = "City Gate"
        self.cost = 3

    def hook_start_turn(self, game, player):
        player.pickup_card()
        card = player.cardSel(
            force=True,
            cardsrc="hand",
            prompt="Put a card from your hand onto your deck",
        )
        player.addCard(card[0], "topdeck")
        player.hand.remove(card[0])


###############################################################################
class Test_CityGate(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=["City Gate"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project("City Gate")
        self.plr.set_deck("Gold")
        self.plr.set_hand("Copper", "Estate", "Province", "Silver", "Duchy")
        self.plr.test_input = ["Select Province"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.deck[-1].name, "Province")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
