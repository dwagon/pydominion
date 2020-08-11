#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Cellar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+1 Action; Discard any number of cards. +1 card per card discarded."
        self.name = 'Cellar'
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        todiscard = player.plrDiscardCards(0, anynum=True, prompt="Discard any number of cards and gain one per card discarded")
        player.pickupCards(len(todiscard))


###############################################################################
class Test_Cellar(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cellar'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g['Cellar'].remove()

    def test_none(self):
        self.plr.setHand('Estate', 'Copper', 'Silver')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.hand.size(), 3)

    def test_one(self):
        self.plr.setHand('Estate', 'Copper', 'Silver')
        self.plr.setDeck('Province', 'Gold')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['discard estate', 'finish']
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.deck[-1].name, 'Province')
        self.assertIsNotNone(self.plr.in_hand('Gold'))
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
