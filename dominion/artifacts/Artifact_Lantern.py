#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Artifact


###############################################################################
class Artifact_Lantern(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "Your Border Guards reveal 3 cards and discard 2. (It takes all 3 being Actions to take the Horn.)"
        self.name = "Lantern"


###############################################################################
class Test_Lantern(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initartifacts=["Lantern"],
            initcards=["Border Guard", "Moat", "Guide"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.artifact = self.g.artifacts["Lantern"]
        self.card = self.g["Border Guard"].remove()
        self.plr.assign_artifact("Lantern")

    def test_play(self):
        self.plr.setDeck("Province", "Silver", "Gold")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Select Gold"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Province"))

    def test_play_actions(self):
        self.plr.setDeck("Guide", "Moat", "Guide")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Select Moat", "Take Horn"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_hand("Moat"))
        self.assertIsNotNone(self.plr.in_discard("Guide"))
        self.assertTrue(self.plr.has_artifact("Horn"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
