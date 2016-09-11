#!/usr/bin/env python

import unittest
from Landmark import Landmark
from collections import defaultdict


###############################################################################
class Landmark_TriumphalArch(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When scoring, 3VP per copy you have of the 2nd most common Action card among your cards (if it's a tie, count either)."""
        self.name = "Triumphal Arch"

    def hook_end_of_game(self, game, player):
        cards = defaultdict(int)
        for card in player.allCards():
            if card.isAction():
                cards[card.name] += 1
        nums = sorted(cards.values())
        player.addScore('Triumphal Arch', nums[-2] * 3)


###############################################################################
class Test_TriumphalArch(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Triumphal Arch'], initcards=['Moat', 'Militia'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_play(self):
        """ Test Triumphal Arch"""
        self.plr.setHand('Moat', 'Moat', 'Moat')
        self.plr.setDeck('Militia', 'Militia', 'Militia', 'Militia')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Triumphal Arch'], 3 * 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
