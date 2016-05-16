#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Dungeon(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'adventure'
        self.desc = "+1 Action. Now and next turn: +2 cards then discard 2 cards"
        self.name = 'Dungeon'
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        self.sifter(game, player)

    def duration(self, game, player):
        self.sifter(game, player)

    def sifter(self, game, player):
        """ +2 Cards, then discard 2 cards. """
        player.pickupCards(2)
        player.plrDiscardCards(num=2)


###############################################################################
class Test_Dungeon(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['dungeon'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['dungeon'].remove()

    def test_playcard(self):
        """ Play a dungeon """
        self.plr.setDeck('estate', 'estate', 'estate', 'estate', 'estate', 'silver', 'gold')
        self.plr.setHand('province', 'duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['province', 'duchy', 'finish']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 2)   # 2 picked up from dungeon -2 discard
        self.assertIsNone(self.plr.inHand('duchy'))
        self.assertEquals(self.plr.durationSize(), 1)
        self.assertEquals(self.plr.discardSize(), 2)
        self.plr.endTurn()
        self.plr.test_input = ['1', '2', 'finish']
        self.plr.startTurn()
        self.assertEquals(self.plr.durationSize(), 0)
        self.assertEquals(self.plr.playedSize(), 1)
        self.assertEquals(self.plr.played[-1].name, 'Dungeon')
        self.assertEquals(self.plr.discardSize(), 2)
        self.assertEquals(self.plr.handSize(), 5)   # 5 dealt + 2 from dungeon -2 discard


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
