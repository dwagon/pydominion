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
        player.plrDiscardCards(num=2, force=True)


###############################################################################
class Test_Dungeon(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Dungeon'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Dungeon'].remove()

    def test_playcard(self):
        """ Play a dungeon """
        self.plr.setDeck('Estate', 'Estate', 'Estate', 'Estate', 'Estate', 'Silver', 'Gold')
        self.plr.setHand('Province', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['province', 'duchy', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)   # 2 picked up from dungeon -2 discard
        self.assertIsNone(self.plr.inHand('duchy'))
        self.assertEqual(self.plr.durationSize(), 1)
        self.assertEqual(self.plr.discardSize(), 2)
        self.plr.endTurn()
        self.plr.test_input = ['1', '2', 'finish']
        self.plr.startTurn()
        self.assertEqual(self.plr.durationSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)
        self.assertEqual(self.plr.played[-1].name, 'Dungeon')
        self.assertEqual(self.plr.discardSize(), 2)
        self.assertEqual(self.plr.handSize(), 5)   # 5 dealt + 2 from dungeon -2 discard


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
