#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Fugitive(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = "+1 Action, +2 Cards, Discard a card"
        self.name = 'Fugitive'
        self.purchasable = False
        self.actions = 1
        self.cards = 2
        self.cost = 4

    def special(self, game, player):
        player.plrDiscardCards(num=1)

    def hook_discardCard(self, game, player):
        """ Replace with Warrior """
        player.replace_traveller(self, 'Disciple')


###############################################################################
class Test_Fugitive(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Fugitive'].remove()

    def test_fugitive(self):
        """ Play a fugitive """
        self.plr.setHand('Province')
        self.plr.test_input = ['province']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertEqual(self.plr.handSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
