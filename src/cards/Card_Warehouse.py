#!/usr/bin/env python

import unittest
from Card import Card


class Card_Warehouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = "+3 cards, +1 action, discard 3 cards"
        self.name = 'Warehouse'
        self.cards = 3
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard 3 cards"""
        player.plrDiscardCards(3)


###############################################################################
class Test_Warehouse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Warehouse'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Warehouse'].remove()

    def test_playcard(self):
        """ Play a warehouse """
        self.plr.setHand('Estate', 'Copper', 'Silver', 'Gold')
        self.plr.setDeck('Province', 'Province', 'Province', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['discard estate', 'discard copper', 'discard duchy', 'finish']
        self.plr.playCard(self.card)
        # Initial hand size - 3 discards + 3 pickups - 1 played
        self.assertEquals(self.plr.handSize(), 5 - 3 + 3 - 1)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertEquals(self.plr.discardSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
