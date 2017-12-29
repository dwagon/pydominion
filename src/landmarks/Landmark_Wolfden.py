#!/usr/bin/env python

import unittest
from Landmark import Landmark
from collections import defaultdict


###############################################################################
class Landmark_WolfDen(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When scoring, -3VP per card you have exactly one copy of."""
        self.name = "Wolf Den"

    def hook_end_of_game(self, game, player):
        score = 0
        cards = defaultdict(int)
        for card in player.allCards():
            cards[card.name] += 1
        for card, num in cards.items():
            if num == 1:
                score -= 3
                player.output("Wolf Den: -3 due to only one %s" % card)
        player.addScore('Wolf Den', score)


###############################################################################
class Test_WolfDen(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Wolf Den'], badcards=['Shepherd', 'Pooka', 'Fool', 'Tracker', 'Cemetery', 'Pixie', 'Secret Cave'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Wolf Den """
        self.plr.setDiscard('Gold', 'Silver')
        self.plr.gameOver()
        try:
            self.assertEqual(self.plr.getScoreDetails()['Wolf Den'], -6)
        except AssertionError:
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
