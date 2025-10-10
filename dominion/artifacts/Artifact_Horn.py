#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Horn"""
import unittest

from dominion import Artifact
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Artifact_Horn(Artifact.Artifact):
    """Horn Artifact"""

    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "Once per turn, when you discard a Border Guard from play, you may put it onto your deck."
        self.name = "Horn"


###############################################################################
class Test_Horn(unittest.TestCase):
    """Test Horn"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Border Guard"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.artifact = self.g.artifacts["Horn"]
        self.card = self.g.get_card_from_pile("Border Guard")

    def test_horn(self):
        """Test Horn"""
        self.plr.assign_artifact("Horn")
        self.plr.test_input = ["Put onto deck"]
        self.plr.discard_card(self.card)
        self.assertIn("Border Guard", self.plr.piles[Piles.DECK])
        self.assertNotIn("Border Guard", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
