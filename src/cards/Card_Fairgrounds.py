#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Fairgrounds(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'cornucopia'
        self.desc = "2VP / 5 card types"
        self.name = 'Fairgrounds'
        self.playable = False
        self.cost = 6

    def special_score(self, game, player):
        """ Worth 2VP for every 5 differently named cards in your deck (round down)"""
        numtypes = set([c.name for c in player.allCards()])
        return 2 * int(len(numtypes) / 5)


###############################################################################
class Test_Fairgrounds(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['fairgrounds'])
        self.plr = self.g.playerList(0)
        self.card = self.g['fairgrounds'].remove()

    def test_zero(self):
        """ Fairground for 4 types """
        self.plr.setDeck('copper', 'estate', 'silver', 'fairgrounds')
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Fairgrounds'], 0)

    def test_one(self):
        """ Fairground for 4 types """
        self.plr.setDeck('copper', 'estate', 'silver', 'fairgrounds', 'gold')
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Fairgrounds'], 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
