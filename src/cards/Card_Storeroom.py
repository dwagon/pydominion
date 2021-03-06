#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Storeroom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Buy; Discard any number of cards. +1 Card per card
            discarded. Discard any number of cards. +1 Coin per card discarded
            the second time """
        self.name = 'Store Room'
        self.buys = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard any number of cards. +1 Card per card discarded.
            Discard any number of cards. +1 Coin per card discarded the
            second time"""
        todiscard = player.plrDiscardCards(0, anynum=True, prompt="Discard any number of cards. +1 Card per card discarded")
        player.output("Gaining %d cards from Storeroom" % len(todiscard))
        player.pickupCards(len(todiscard))
        player.output("Discard any number of cards. +1 Coin per card discarded")
        todiscard = player.plrDiscardCards(0, anynum=True)
        player.output("Gaining %d coins from Storeroom" % len(todiscard))
        player.addCoin(len(todiscard))


###############################################################################
class Test_Storeroom(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Store Room'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Store Room'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a store room """
        self.plr.test_input = ['0', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_discardonce(self):
        """ Storeroom: Only discard during the first discard phase """
        self.plr.test_input = ['1', '0', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 - 1 + 1)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_discardtwice(self):
        """ Storeroom: Discard during the both discard phases """
        self.plr.test_input = ['1', '0', '1', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 - 1)
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
