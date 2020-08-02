#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Monastery(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'night'
        self.base = 'nocturne'
        self.desc = "For each card you've gained this turn, you may trash a card from your hand or a Copper you have in play."
        self.name = 'Monastery'
        self.cost = 2

    def night(self, game, player):
        numgained = len(player.stats['gained'])
        if not numgained:
            return
        selectfrom = player.hand + [_ for _ in player.played if _.name == 'Copper']
        player.plrTrashCard(num=numgained, cardsrc=selectfrom)


###############################################################################
class Test_Monastery(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Monastery'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.monastery = self.g['Monastery'].remove()

    def test_play_card(self):
        """ Play Monastery """
        self.plr.phase = 'night'
        self.plr.setHand('Duchy')
        self.plr.addCard(self.monastery, 'hand')
        self.plr.gainCard('Silver')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.monastery)
        self.assertIsNotNone(self.g.in_trash('Duchy'))

    def test_play_no_gained(self):
        """ Play Monastery when you didn't gain a card """
        self.plr.phase = 'night'
        self.plr.setHand('Duchy')
        self.plr.addCard(self.monastery, 'hand')
        self.plr.playCard(self.monastery)

    def test_play_copper(self):
        """ Play Monastery when you have a copper """
        self.plr.phase = 'night'
        self.plr.setHand('Duchy')
        self.plr.setPlayed('Copper')
        self.plr.addCard(self.monastery, 'hand')
        self.plr.gainCard('Silver')
        self.plr.test_input = ['Copper']
        self.plr.playCard(self.monastery)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
