#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Palace(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When scoring, 3VP per set you have of Copper - Silver - Gold."""
        self.name = "Palace"

    def hook_end_of_game(self, game, player):
        num = {'Copper': 0, 'Silver': 0, 'Gold': 0}
        for card in player.allCards():
            if card.name in num:
                num[card.name] += 1
        score = min(num.values()) * 3
        player.output("Palace scored %d VP (%d Copper, %d Silver, %d Gold)" % (score, num['Copper'], num['Silver'], num['Gold']))
        player.addScore('Palace', score)


###############################################################################
class Test_Palace(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Palace'])
        self.g.start_game()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Palace """
        self.plr.setDiscard('Gold', 'Silver', 'Silver', 'Copper', 'Duchy')
        self.plr.setDeck('Gold', 'Silver', 'Copper', 'Copper', 'Duchy')
        self.plr.setHand('Silver', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Palace'], 2 * 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
