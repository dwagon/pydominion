#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Mill(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.name = 'Mill'
        self.desc = "+1 Card; +1 Action; You may discard 2 cards, for +2 Coin; 1VP"
        self.cost = 4
        self.actions = 1
        self.victory = 1
        self.cards = 1

    def special(self, game, player):
        dc = player.plrDiscardCards(num=2)
        if len(dc) == 2:
            player.addCoin(2)


###############################################################################
class Test_Mill(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Mill'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Mill'].remove()

    def test_play(self):
        self.plr.setHand('Gold', 'Silver')
        self.plr.test_input = ['Discard Gold', 'Finish']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1 + 1)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getScoreDetails()['Mill'], 1)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))

    def test_discard(self):
        self.plr.setHand('Gold', 'Silver')
        self.plr.test_input = ['Discard Gold', 'Discard Silver', 'Finish']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
