#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Smithy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "+3 cards"
        self.name = 'Smithy'
        self.cards = 3
        self.cost = 4


###############################################################################
class Test_Smithy(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Smithy'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Smithy'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the smithy """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
