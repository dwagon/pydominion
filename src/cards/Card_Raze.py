#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Raze(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.ADVENTURE
        self.desc = """+1 Action; Trash this or a card from your hand. Look at a number
            of cards from the top of your deck equal to the cost in Coin of the
            trashed card. Put one into your hand and discard the rest """
        self.name = 'Raze'
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """ Trash this or a card from your hand. Look at a number of cards
            from the top of your deck equal to the cost in Coin of the trashed
            card. Put one into your hand and discard the rest """
        cards_to_trash = [self]
        for c in player.hand:
            cards_to_trash.append(c)
        trash = player.plrTrashCard(cardsrc=cards_to_trash, force=True)
        cost = trash[0].cost
        if cost:
            cards = []
            for c in range(cost):
                cards.append(player.nextCard())
            ans = player.cardSel(force=True, prompt="Pick a card to put into your hand", cardsrc=cards)
            for c in cards:
                if c == ans[0]:
                    player.addCard(c, 'hand')
                else:
                    player.addCard(c, 'discard')


###############################################################################
class Test_Raze(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Raze'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Raze'].remove()

    def test_play(self):
        """ Play a raze - trashing itself """
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Silver', 'Gold', 'Province')
        self.plr.test_input = ['Raze', 'Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.discard_size(), 1)
        self.assertIsNotNone(self.plr.in_discard('Province'))
        self.assertIsNotNone(self.plr.in_hand('Gold'))
        self.assertIsNotNone(self.plr.in_deck('Silver'))
        self.assertIsNotNone(self.g.in_trash('Raze'))

    def test_copper(self):
        """ Play a raze - trashing copper - a zero value card """
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Silver', 'Gold', 'Province')
        self.plr.test_input = ['Copper', 'Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.g.in_trash('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
