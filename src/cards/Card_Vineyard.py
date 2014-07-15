#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Vineyard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'alchemy'
        self.desc = "num action cards / 3 VP"
        self.name = 'Vineyard'
        self.playable = False
        self.cost = 0
        self.potcost = 1

    def special_score(self, game, player):
        """ Worth 1VP for every 3 action cards in your deck rounded down """
        score = 0
        for c in player.allCards():
            if c.isAction():
                score += 1
        return score / 3


###############################################################################
class Test_Vineyard(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['vineyard', 'moat'])
        self.plr = list(self.g.players.values())[0]

    def test_scoreOne(self):
        self.plr.setHand('vineyard')
        self.plr.setDeck('copper')
        self.plr.setDiscard('moat', 'moat', 'moat', 'moat')
        self.assertEquals(self.plr.getScoreDetails()['Vineyard'], 1)

    def test_scoreTwo(self):
        self.plr.setHand('vineyard')
        self.plr.setDeck('vineyard')
        self.plr.setDiscard('moat', 'moat', 'moat', 'moat', 'moat', 'moat')
        self.assertEquals(self.plr.getScoreDetails()['Vineyard'], 4)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
