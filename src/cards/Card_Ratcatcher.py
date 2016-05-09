#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Ratcatcher(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reserve']
        self.base = 'adventure'
        self.desc = "+1 Card, +1 Action; Call to trash a card"
        self.name = 'Ratcatcher'
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        player.played.remove(self)
        player.addCard(self, 'reserve')

    def hook_callReserve(self, game, player):
        """ At the start of your turn, you may call this, to trash a
            card from your hand """
        player.plrTrashCard()


###############################################################################
class Test_Ratcatcher(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['ratcatcher'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['ratcatcher'].remove()

    def test_play(self):
        """ Play a ratcatcher """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.plr.reserveSize(), 1)
        c = self.plr.inReserve('Ratcatcher')
        self.assertEqual(c.name, 'Ratcatcher')

    def test_call(self):
        """ Call from Reserve"""
        self.plr.setHand('gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['gold']
        self.plr.playCard(self.card)
        c = self.plr.callReserve('Ratcatcher')
        self.assertEqual(c.name, 'Ratcatcher')
        self.assertEqual(self.g.trashSize(), 1)
        self.assertEqual(self.g.trashpile[0].name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
