#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Villa(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.name = 'Villa'
        self.cost = 4
        self.actions = 2
        self.buys = 1
        self.coin = 1

    def desc(self, player):
        if player.phase == 'action':
            return "+2 Actions; +1 Buy; +1 Coin"
        else:
            return "+2 Actions; +1 Buy; +1 Coin; When you gain this, put it into your hand, +1 Action, and if it's your Buy phase return to your Action phase."

    def hook_gain_this_card(self, game, player):
        if player.phase == 'buy':
            player.phase = 'action'
        player.addActions(1)
        return {'destination': 'hand'}


###############################################################################
class Test_Villa(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Villa'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Villa'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 2)

    def test_gain(self):
        self.plr.phase = 'buy'
        self.plr.gainCard('Villa')
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.phase, 'action')
        self.assertIsNotNone(self.plr.inHand('Villa'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
