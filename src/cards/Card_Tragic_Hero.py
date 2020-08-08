#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Tragic_Hero(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.NOCTURNE
        self.desc = "+3 Cards; +1 Buys; If you have 8 or more cards in hand (after drawing), trash this and gain a Treasure."
        self.name = 'Tragic Hero'
        self.cost = 5
        self.cards = 3
        self.buys = 1

    def special(self, game, player):
        if player.handSize() >= 8:
            player.trashCard(self)
            player.plrGainCard(cost=None, types={Card.TREASURE: True})


###############################################################################
class Test_Tragic_Hero(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tragic Hero'], badcards=["Fool's Gold"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Tragic Hero'].remove()

    def test_play(self):
        """ Play a Tragic Hero with less than 8 cards """
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 1 + 1)
        self.assertEqual(self.plr.handSize(), 1 + 3)

    def test_gainsomething(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Get Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 3)
        self.assertIsNotNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
