#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Den_of_Sin(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = 'nocturne'
        self.name = 'Den of Sin'
        self.cost = 2

    def desc(self, player):
        if player.phase == 'buy':
            return "At the start of your next turn, +2 Cards; This is gained to your hand (instead of your discard pile)."
        else:
            return "At the start of your next turn, +2 Cards"

    def duration(self, game, player):
        for i in range(2):
            player.pickupCard()

    def hook_gainThisCard(self, game, player):
        return {'destination': 'hand'}


###############################################################################
class Test_Den_of_Sin(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Den of Sin'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Den of Sin'].remove()

    def test_gain(self):
        self.plr.gainCard('Den of Sin')
        self.assertIsNotNone(self.plr.inHand('Den of Sin'))

    def test_duration(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
