#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Tactician(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "Discard hand; +5 cards, +1 buy and +1 action next turn"
        self.name = 'Tactician'
        self.cost = 5

    def special(self, game, player):
        self.discarded = False
        discard = player.plrChooseOptions(
            'Discard hand for good stuff next turn?',
            ('Discard', True),
            ('Keep', False)
        )
        if discard and player.handSize():
            self.discarded = True
            player.discardHand()

    def duration(self, game, player):
        """ +5 Cards, +1 Buy, +1 Action """
        if self.discarded:
            player.pickupCards(5)
            player.addBuys(1)
            player.addActions(1)
            self.discarded = False


###############################################################################
class Test_Tactician(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tactician'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Tactician'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_discard(self):
        """ Play a tactician and discard hand"""
        self.plr.test_input = ['discard']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 0)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEquals(self.plr.handSize(), 10)
        self.assertEquals(self.plr.getActions(), 2)
        self.assertEquals(self.plr.getBuys(), 2)

    def test_play_keep(self):
        """ Play a tactician and discard hand"""
        self.plr.test_input = ['keep']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertEquals(self.plr.getBuys(), 1)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
