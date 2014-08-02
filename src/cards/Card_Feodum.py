#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Feodum(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'darkages'
        self.desc = "1VP / 3 silvers - trash for 3 silvers"
        self.name = 'Feodum'
        self.cost = 4

    def special_score(self, game, player):
        """ Worth 1VP for every 3 silvers cards in your deck rounded down """
        numsilver = 0
        for c in player.allCards():
            if c.name == 'Silver':
                numsilver += 1
        return int(numsilver / 3)

    def hook_trashThisCard(self, game, player):
        """ When you trash this gain 3 silvers """
        for i in range(3):
            player.gainCard('silver')


###############################################################################
class Test_Feodum(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['feodum'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_scoreOne(self):
        self.plr.setHand('feodum')
        self.plr.setDeck('copper')
        self.plr.setDiscard('silver', 'silver', 'silver', 'silver')
        self.assertEquals(self.plr.getScoreDetails()['Feodum'], 1)

    def test_scoreTwo(self):
        self.plr.setHand('feodum')
        self.plr.setDeck('feodum')
        self.plr.setDiscard('silver', 'silver', 'silver', 'silver', 'silver', 'silver')
        self.assertEquals(self.plr.getScoreDetails()['Feodum'], 4)

    def test_trash(self):
        """ Trash a feodum card """
        card = self.g['feodum'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.trashCard(card)
        self.assertEquals(self.plr.discardSize(), 3)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Silver')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
