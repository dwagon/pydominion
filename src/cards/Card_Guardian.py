#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Guardian(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = Game.NOCTURNE
        self.desc = """Until your next turn, when another player plays an
            Attack card, it doesn't affect you. At the start of your next turn,
            +1 Coin."""
        self.name = 'Guardian'
        self.defense = True
        self.cost = 2

    def duration(self, game, player):
        player.addCoin(1)

    def hook_gain_this_card(self, game, player):
        return {'destination': 'hand'}


###############################################################################
class Test_Guardian(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Guardian'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Guardian'].remove()

    def test_gain(self):
        self.plr.gainCard('Guardian')
        self.assertIsNotNone(self.plr.in_hand('Guardian'))

    def test_duration(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
