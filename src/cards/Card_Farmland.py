#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Farmland(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'hinterlands'
        self.desc = "2VP; trash a card when bought and gain another"
        self.name = 'Farmland'
        self.cost = 6
        self.victory = 2

    def hook_gainThisCard(self, game, player):
        """ When you buy this, trash a card from your hand.
        Gain a card costing exactly 2 more than the trashed card
        """
        c = player.plrTrashCard(force=True)
        player.plrGainCard(cost=c[0].cost + 2, modifier='equal')


###############################################################################
class Test_Farmland(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['farmland', 'militia'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['farmland'].remove()

    def test_gain(self):
        """ Gain a farmland """
        self.plr.setHand('estate', 'estate')
        self.plr.test_input = ['1', '1']
        self.plr.gainCard('farmland')
        self.assertEqual(self.g.trashSize(), 1)
        self.assertEqual(self.plr.handSize(), 1)
        # 1 for farmland, 1 for gained card
        self.assertEqual(self.plr.discardSize(), 2)

    def test_score(self):
        self.plr.setDeck('farmland')
        sd = self.plr.getScoreDetails()
        self.assertEquals(sd['Farmland'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
