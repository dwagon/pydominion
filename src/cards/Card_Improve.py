#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Improve(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.RENAISSANCE
        self.desc = """+2 Coin; At the start of Clean-up, you may trash an Action
        card you would discard from play this turn, to gain a card costing exactly
        1 more than it."""
        self.name = 'Improve'
        self.cost = 3
        self.coin = 2

    def hook_cleanup(self, game, player):
        acts = [_ for _ in player.hand + player.discardpile if _.isAction()]
        if not acts:
            return
        tt = player.plrTrashCard(cardsrc=acts, prompt="Trash a card through Improve")
        if not tt:
            return
        cost = tt[0].cost
        player.plrGainCard(cost+1, modifier='equal')


###############################################################################
class Test_Improve(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Improve', 'Moat', 'Guide'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Improve'].remove()

    def test_play(self):
        self.plr.setHand('Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.test_input = ['End phase', 'End phase', 'Trash Moat', 'Get Guide']
        self.plr.turn()
        self.assertIsNotNone(self.g.in_trash('Moat'))
        self.assertIsNotNone(self.plr.in_discard('Guide'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
