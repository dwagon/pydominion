#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Altar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DARKAGES
        self.desc = """Trash a card from your hand. Gain a card costing up to 5 Coin."""
        self.name = 'Altar'
        self.cost = 6

    def special(self, game, player):
        # Trash a card from your hand
        player.plrTrashCard(prompt="Trash a card from your hand", force=True)

        # Gain a card costing up to 5 Coin
        player.plrGainCard(5)


###############################################################################
class Test_Altar(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Altar', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Altar'].remove()

    def test_play(self):
        """ Play an Altar"""
        self.plr.setHand('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Province', 'Moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Moat'))
        self.assertIsNotNone(self.g.in_trash('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
