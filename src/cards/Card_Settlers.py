#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Settlers(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.EMPIRES
        self.name = 'Settlers'
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.desc = """+1 Card +1 Action. Look through your discard pile. You may reveal a Copper from it and put it into your hand."""

    def special(self, game, player):
        cu = player.in_discard('Copper')
        if cu:
            player.addCard(cu, 'hand')
            player.discardpile.remove(cu)
            player.revealCard(cu)
            player.output("Pulled Copper from discard into hand")
        else:
            player.output("No Copper in discard")


###############################################################################
class Test_Settlers(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Settlers'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Settlers'].remove()

    def test_play(self):
        """ Play a Settlers and pull a copper"""
        self.plr.setDiscard('Gold', 'Silver', 'Copper')
        self.plr.setHand('Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_hand('Copper'))
        self.assertIsNone(self.plr.in_discard('Copper'))
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 2 + 1 + 1)

    def test_play_nocopper(self):
        """ Play a Settlers and pull a copper"""
        self.plr.setDeck('Gold', 'Silver')
        self.plr.setDiscard('Gold', 'Silver', 'Duchy')
        self.plr.setHand('Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_hand('Copper'))
        self.assertEqual(self.plr.handSize(), 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
