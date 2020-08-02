#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Margrave(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = """+3 Card +1 Buy. Each other player draws a card, then discards down to 3 cards in hand"""
        self.name = 'Margrave'
        self.cards = 3
        self.buys = 1
        self.cost = 5

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.output("Due to %s's Margrave gain a card then discard down to 3" % player.name)
            plr.pickupCard()
            plr.plrDiscardDownTo(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Margrave(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Margrave'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Margrave'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the card """
        self.vic.test_input = ['1', '2', '3', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.vic.handSize(), 3)
        self.assertEqual(self.plr.handSize(), 5 + 3)
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
