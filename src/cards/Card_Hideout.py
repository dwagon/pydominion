#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Hideout(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'renaissance'
        self.desc = """+1 Card; +2 Actions; Trash a card from your hand. If it's a Victory card, gain a Curse."""
        self.name = 'Hideout'
        self.required_cards = ['Curse']
        self.actions = 2
        self.cards = 1
        self.cost = 4

    ###########################################################################
    def special(self, game, player):
        card = player.plrTrashCard(num=1)
        if card[0].isVictory():
            player.gainCard('Curse')


###############################################################################
class Test_Hideout(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hideout'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_playCard(self):
        self.plr.setDeck('Silver')
        self.plr.setHand('Copper', 'Estate')
        self.card = self.g['Hideout'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Copper']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2+1)
        self.assertEqual(self.plr.handSize(), 2)

    def test_trashVictory(self):
        self.plr.setDeck('Silver')
        self.plr.setHand('Copper', 'Estate')
        self.card = self.g['Hideout'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Estate']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2+1)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertIsNotNone(self.plr.inDiscard('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
