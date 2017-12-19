#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pouch(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'victory', 'heirloom']
        self.base = 'nocturne'
        self.desc = "+1 Coin; Worth 1VP per Estate you have"
        self.name = 'Pouch'
        self.cost = 2
        self.coin = 1
        self.purchasable = False

    def special_score(self, game, player):
        estates = sum([1 for _ in player.allCards() if _.name == "Estate"])
        return estates


###############################################################################
class Test_Pouch(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tracker'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Pouch'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_score(self):
        self.plr.setHand('Estate', 'Pouch')
        self.plr.setDeck('Estate')
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Pouch'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF