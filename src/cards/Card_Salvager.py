#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Salvager(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """+1 Buy. Trash a card from your hand. Gain Coins equal to its cost."""
        self.name = 'Salvager'
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        card = player.plrTrashCard(force=True)
        player.output("Gained %d coin" % card[0].cost)
        player.addCoin(card[0].cost)


###############################################################################
class Test_Salvager(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Salvager'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Salvager'].remove()

    def test_play(self):
        """ Play a salvage """
        self.plr.setHand('Duchy', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNotNone(self.g.in_trash('Duchy'))
        self.assertEqual(self.plr.getCoin(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
