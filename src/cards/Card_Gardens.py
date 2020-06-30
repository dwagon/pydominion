#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Gardens(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "numcards / 10 VP"
        self.name = 'Gardens'
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """ Worth 1VP for every 10 cards in your deck rounded down """
        numcards = len(player.allCards())
        return int(numcards / 10)


###############################################################################
class Test_Gardens(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Gardens'])
        self.g.start_game()
        self.plr = self.g.playerList(0)

    def test_score_0(self):
        self.plr.setHand('Gardens', 'Copper', 'Copper')
        self.plr.setDeck('Copper', 'Copper', 'Copper')
        self.plr.setDiscard('Copper', 'Copper', 'Copper')
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Gardens'], 0)

    def test_score_1(self):
        self.plr.setHand('Gardens', 'Copper', 'Copper')
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper')
        self.plr.setDiscard('Copper', 'Copper', 'Copper')
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Gardens'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
