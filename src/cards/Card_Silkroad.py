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
        self.playable = False
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Silk Road'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_scoreOne(self):
        self.plr.setHand('Silk Road')
        self.plr.setDeck('Copper')
        self.plr.setDiscard('Estate', 'Estate', 'Estate', 'Estate')
        self.assertEqual(self.plr.getScoreDetails()['Silk Road'], 1)

    def test_scoreTwo(self):
        """ Score for having two silk roads worth two each """
        self.plr.setHand('Silk Road', 'Estate')
        self.plr.setDeck('Estate', 'Estate', 'Silk Road')
        self.plr.setDiscard('Estate', 'Estate', 'Estate', 'Estate', 'Estate')
        self.assertEqual(self.plr.getScoreDetails()['Silk Road'], 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
