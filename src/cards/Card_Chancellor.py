#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Chancellor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+2 coin, Discard deck"
        self.name = 'Chancellor'
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        """ You may immediately put your deck into your discard pile """
        ans = player.plrChooseOptions("Discard deck?", ("Don't Discard", False), ("Discard Deck", True))
        if ans:
            for c in player.deck[:]:
                player.addCard(c, 'discard')
                player.deck.remove(c)


###############################################################################
class Test_Chancellor(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['chancellor'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.ccard = self.g['chancellor'].remove()
        self.plr.setHand('estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_nodiscard(self):
        self.plr.setDeck('copper', 'silver', 'gold')
        self.plr.setDiscard('estate', 'duchy', 'province')
        self.plr.test_input = ["Don't discard"]
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.getCoin(), 2)
        self.assertEquals(self.plr.deckSize(), 3)
        self.assertEquals(self.plr.discardSize(), 3)

    def test_discard(self):
        self.plr.setDeck('copper', 'silver', 'gold')
        self.plr.setDiscard('estate', 'duchy', 'province')
        self.plr.test_input = ['discard deck']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.getCoin(), 2)
        self.assertEquals(self.plr.deckSize(), 0)
        self.assertEquals(self.plr.discardSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
