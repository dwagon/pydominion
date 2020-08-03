#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Legionary(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'empires'
        self.desc = """+3 Coin. You may reveal a Gold from your hand.
            If you do, each other player discards down to 2 cards in hand, then draws a card."""
        self.name = 'Legionary'
        self.cost = 5
        self.coin = 3

    def special(self, game, player):
        au = player.inHand('Gold')
        if au:
            player.revealCard(au)
            for plr in player.attackVictims():
                plr.output("%s's Legionary forces you to discard down to 2" % player.name)
                plr.plrDiscardDownTo(2)
                plr.pickupCard()


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 2
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Legionary(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Legionary'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Legionary'].remove()

    def test_play(self):
        """ Play a Legionary """
        self.plr.setHand('Gold')
        self.victim.test_input = ['1', '2', '3', '0']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertEqual(self.victim.handSize(), 3)
        self.assertEqual(self.victim.discardSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
