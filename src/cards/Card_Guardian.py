#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Guardian(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = 'nocturne'
        self.desc = "Until your next turn, when another player plays an Attack card, it doesn't affect you. At the start of your next turn, +1 Coin."
        self.name = 'Guardian'
        self.defense = True
        self.cost = 2

    def duration(self, game, player):
        player.addCoin(1)

    def hook_gainThisCard(self, game, player):
        return {'destination': 'hand'}


###############################################################################
class Test_Guardian(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Guardian'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Guardian'].remove()

    def test_gain(self):
        self.plr.gainCard('Guardian')
        self.assertIsNotNone(self.plr.inHand('Guardian'))

    def test_duration(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
