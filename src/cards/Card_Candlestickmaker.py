#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Candlestickmaker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.GUILDS
        self.desc = "+1 action, +1 buy, +1 coffer"
        self.name = 'Candlestick Maker'
        self.actions = 1
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        """ Take a Coin Token """
        player.gainCoffer(1)


###############################################################################
class Test_Candlestickmaker(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Candlestick Maker'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Candlestick Maker'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a candlestick maker """
        self.plr.coffer = 0
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoffer(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
