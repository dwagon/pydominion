#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Vassal(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.name = 'Vassal'
        self.coin = 2
        self.cost = 3
        self.desc = "+2 Coin; Discard the top card of your deck. If it is an Action card, you may play it."

    def special(self, game, player):
        card = player.nextCard()
        player.revealCard(card)
        if card.isAction():
            player.addCard(card, 'hand')
            player.playCard(card, costAction=False)
        else:
            player.addCard(card, 'discard')


###############################################################################
class Test_Vassal(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Vassal', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Vassal'].remove()

    def test_play_action(self):
        """ Play a Vassal with action next"""
        self.plr.setDeck('Silver', 'Gold', 'Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.plr.inPlayed('Moat'))
        self.assertEqual(self.plr.handSize(), 5 + 2)

    def test_play_non_action(self):
        """ Play a Vassal with non-action next"""
        self.plr.setDeck('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertEqual(self.plr.handSize(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
