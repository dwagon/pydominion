#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_RuinedLibrary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.desc = "+1 Card"
        self.purchasable = False
        self.cost = 0
        self.name = "Ruined Library"
        self.cards = 1


###############################################################################
class Test_RuinedLibrary(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=4, initcards=['Cultist'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Ruins'].remove()
            if self.card.name == 'Ruined Library':
                break
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a ruined library """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5+1)
# EOF
