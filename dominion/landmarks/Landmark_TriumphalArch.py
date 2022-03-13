#!/usr/bin/env python

import unittest
from collections import defaultdict
from dominion import Game, Landmark


###############################################################################
class Landmark_TriumphalArch(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """When scoring, 3VP per copy you have of the 2nd most common
        Action card among your cards (if it's a tie, count either)."""
        self.name = "Triumphal Arch"

    def hook_end_of_game(self, game, player):
        cards = defaultdict(int)
        for card in player.allCards():
            if card.isAction():
                cards[card.name] += 1
        nums = sorted(cards.values())
        try:
            player.addScore("Triumphal Arch", nums[-2] * 3)
        except IndexError:
            player.output("No score from Triumphal Arch as insufficient action cards")


###############################################################################
class Test_TriumphalArch(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            landmarkcards=["Triumphal Arch"],
            initcards=["Moat", "Militia"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Test Triumphal Arch"""
        self.plr.set_hand("Moat", "Moat", "Moat")
        self.plr.setDeck("Militia", "Militia", "Militia", "Militia")
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()["Triumphal Arch"], 3 * 3)

    def test_noactions(self):
        """Test Triumphal Arch"""
        self.plr.set_hand("Copper", "Copper", "Copper")
        self.plr.setDeck("Duchy", "Duchy", "Duchy", "Duchy")
        self.plr.gameOver()
        sd = self.plr.getScoreDetails()
        self.assertNotIn("Triumphal Arch", sd)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
