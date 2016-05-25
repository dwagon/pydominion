#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Rats(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 Card, +1 Action, Gain a Rats, Trash a non-Rats"
        self.name = 'Rats'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Gain a Rats. Trash a card from your hand other than a Rats. """
        player.gainCard('Rats')
        player.plrTrashCard(force=True, exclude=['Rats'])

    def hook_trashThisCard(self, game, player):
        """ When you trash this +1 Card """
        player.pickupCard()


###############################################################################
class Test_Rats(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Rats'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.rats = self.g['Rats'].remove()
        self.plr.setDeck('Estate', 'Province', 'Duchy')
        self.plr.setHand('Copper', 'Gold', 'Silver', 'Rats')
        self.plr.addCard(self.rats, 'hand')

    def test_play(self):
        self.plr.setDeck('Gold')
        self.plr.test_input = ['trash copper']
        self.plr.playCard(self.rats)
        self.plr.addActions(1)
        self.assertEqual(self.plr.hand[-1].name, 'Gold')

    def test_trashcard(self):
        self.plr.test_input = ['trash copper']
        self.plr.playCard(self.rats)
        self.assertEquals(self.g.trashSize(), 1)
        self.assertNotEquals(self.g.trashpile[0].name, 'Rats')

    def test_gainrats(self):
        self.plr.test_input = ['trash copper']
        self.plr.playCard(self.rats)
        self.assertEquals(self.plr.discardpile[0].name, 'Rats')

    def test_trashrats(self):
        """ Trashing Rats - gain another card"""
        handsize = self.plr.handSize()
        self.plr.trashCard(self.rats)
        # Lose rats, gain another card
        self.assertEqual(self.plr.handSize(), handsize)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
