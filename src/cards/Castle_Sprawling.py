#!/usr/bin/env python

import unittest
import Card
import Game
from cards.Card_Castles import CastleCard


###############################################################################
class Card_SprawlingCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.VICTORY, Card.CASTLE]
        self.base = Game.EMPIRES
        self.cost = 8
        self.desc = """4VP. When you gain this, gain a Duchy or 3 Estates."""
        self.victory = 4
        self.name = "Sprawling Castle"

    def hook_gain_this_card(self, game, player):
        ch = player.plrChooseOptions(
            "Gain a Duchy or 3 Estates",
            ("Gain a Duchy", 'duchy'), ("Gain 3 Estates", 'estates')
            )
        if ch == 'duchy':
            player.gainCard('Duchy')
        else:
            for _ in range(3):
                player.gainCard('Estate')


###############################################################################
class Test_SprawlingCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Castles'], badcards=['Duchess'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        """ Play a sprawling castle"""
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Sprawling Castle':
                break
        self.plr.addCard(self.card, 'hand')
        self.assertEqual(self.plr.getScoreDetails()['Sprawling Castle'], 4)

    def test_gain_duchy(self):
        """ Gain duchy through Sprawling Castle """
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Opulent Castle':  # One before Sprawling
                break
        self.plr.test_input = ['duchy']
        self.plr.gainCard('Castles')
        self.assertIsNotNone(self.plr.in_discard('Duchy'))
        self.assertIsNone(self.plr.in_discard('Estate'))
        self.assertEqual(self.plr.discard_size(), 1 + 1)

    def test_gain_estate(self):
        """ Gain estates through Sprawling Castle """
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Opulent Castle':  # One before Sprawling
                break
        self.plr.test_input = ['estates']
        self.plr.gainCard('Castles')
        self.assertIsNone(self.plr.in_discard('Duchy'))
        self.assertIsNotNone(self.plr.in_discard('Estate'))
        self.assertEqual(self.plr.discard_size(), 3 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
