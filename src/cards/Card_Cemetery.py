#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Cemetery(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'nocturne'
        self.desc = "+2 VP; When you gain this, trash up to 4 cards from your hand."
        self.name = 'Cemetery'
        self.cost = 4
        self.victory = 2
        self.heirloom = 'Haunted Mirror'

    def hook_gainThisCard(self, game, player):
        player.plrTrashCard(num=4)


###############################################################################
class Test_Cemetery(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cemetery'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Cemetery'].remove()

    def test_gain(self):
        """ Gain a Cemetery """
        self.plr.setHand('Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province')
        self.plr.test_input = ['Copper', 'Silver', 'Gold', 'Estate', 'Finish']
        self.plr.gainCard('Cemetery')
        self.assertIsNotNone(self.g.inTrash('Copper'))
        self.assertIsNotNone(self.g.inTrash('Gold'))
        self.assertIsNone(self.g.inTrash('Duchy'))
        self.assertEqual(self.plr.getScoreDetails()['Cemetery'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF