#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Shepherd(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'nocturne'
        self.desc = "+1 action; Discard any number of victory cards +2 cards per card discarded"
        self.name = 'Shepherd'
        self.cost = 2
        self.actions = 1
        self.heirloom = 'Pasture'

    def special(self, game, player):
        todiscard = player.plrDiscardCards(num=0, anynum=True, types={'victory': True})
        player.pickupCards(2*len(todiscard))


###############################################################################
class Test_Shepherd(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Shepherd'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Shepherd'].remove()

    def test_play(self):
        """ Play a Shepherd """
        self.plr.setHand('Estate', 'Province', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Estate', 'Duchy', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
