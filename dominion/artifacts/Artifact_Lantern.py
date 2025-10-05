#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Lantern"""
import unittest

from dominion import Artifact
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Artifact_Lantern(Artifact.Artifact):
    """Lantern artifact"""

    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "Your Border Guards reveal 3 cards and discard 2. (It takes all 3 being Actions to take the Horn.)"
        self.name = "Lantern"


###############################################################################
class Test_Lantern(unittest.TestCase):
    """Test Lantern"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initartifacts=["Lantern"],
            initcards=["Border Guard", "Moat", "Guide"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.artifact = self.g.artifacts["Lantern"]
        self.card = self.g.get_card_from_pile("Border Guard")
        self.plr.assign_artifact("Lantern")

    def test_play(self):
        """Test Play"""
        self.plr.piles[Piles.DECK].set("Province", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Province"])

    def test_play_actions(self):
        """Test gaining a horn"""
        self.plr.piles[Piles.DECK].set("Guide", "Moat", "Guide")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat", "Take Horn"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Guide"])
        self.assertTrue(self.plr.has_artifact("Horn"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
