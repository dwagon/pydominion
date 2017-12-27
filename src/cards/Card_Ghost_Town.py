#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Ghost_Town(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = 'nocturne'
        self.name = 'Ghost Town'
        self.desc = "At the start of your next turn, +1 Card and +1 Action. This is gained to your hand (instead of your discard pile)."

    def hook_gainThisCard(self, game, player):
        return {'destination': 'hand'}

    def duration(self, game, player):
        player.pickupCard()
        player.addActions(1)


###############################################################################
class Test_Ghost_Town(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Ghost Town'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.gtown = self.g['Ghost Town'].remove()

    def test_play_card(self):
        """ Play Ghost Town """
        self.plr.addCard(self.gtown, 'hand')
        self.plr.playCard(self.gtown)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getActions(), 2)

    def test_gain(self):
        self.plr.gainCard('Ghost Town')
        self.assertIsNone(self.plr.inDiscard('Ghost Town'))
        self.assertIsNotNone(self.plr.inHand('Ghost Town'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
