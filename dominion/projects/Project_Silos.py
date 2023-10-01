#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Silos(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, discard any number of Coppers, revealed, and draw that many cards."
        self.name = "Silos"
        self.cost = 4

    def hook_start_turn(self, game, player):
        cus = [_ for _ in player.piles[Piles.HAND] if _.name == "Copper"]
        if cus:
            choices = []
            for num in range(len(cus) + 1):
                choices.append((f"Silo: Discard {num} Coppers", num))
            ans = player.plr_choose_options("Discard how many coppers? ", *choices)
            for _ in range(ans):
                cu = player.piles[Piles.HAND]["Copper"]
                player.discard_card(cu)
                player.pickup_cards(1)


###############################################################################
class TestSilos(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Silos"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project("Silos")
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Copper", "Province")
        self.plr.test_input = ["2"]
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
