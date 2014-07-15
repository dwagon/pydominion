#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Silkroad(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'hinterlands'
        self.desc = "num victory cards / 4 VP"
        self.name = 'Silk Road'
        self.cost = 4

    def special_score(self, game, player):
        """ Worth 1VP for every 4 victory cards in your deck rounded down """
        score = 0
        for c in player.allCards():
            if c.isVictory():
                score += 1
        return int(score / 4)


###############################################################################
class Test_Silkroad(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['silkroad'])
        self.plr = list(self.g.players.values())[0]

    def test_scoreOne(self):
        self.plr.setHand('silkroad')
        self.plr.setDeck('copper')
        self.plr.setDiscard('estate', 'estate', 'estate', 'estate')
        self.assertEquals(self.plr.getScoreDetails()['Silk Road'], 1)

    def test_scoreTwo(self):
        """ Score for having two silk roads worth two each """
        self.plr.setHand('silkroad', 'estate')
        self.plr.setDeck('estate', 'estate', 'silkroad')
        self.plr.setDiscard('estate', 'estate', 'estate', 'estate', 'estate')
        self.assertEquals(self.plr.getScoreDetails()['Silk Road'], 2 + 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
