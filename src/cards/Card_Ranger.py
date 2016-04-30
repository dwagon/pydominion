#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Ranger(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = "+1 Buy. Turn your journey over. If its face up +5 Cards"
        self.name = 'Ranger'
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        """ Turn your Journey token over. If it's face up, +5 cards """
        if player.flip_journey_token():
            player.output("Ranger gives +5 Cards")
            player.pickupCards(5)


###############################################################################
class Test_Ranger(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['ranger'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['ranger'].remove()

    def test_play_first(self):
        """ Play a ranger """
        self.plr.journey_token = True
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.handSize(), 0)
        self.assertFalse(self.plr.journey_token)

    def test_play_second(self):
        """ Play a ranger the second time """
        self.plr.journey_token = False
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.plr.journey_token)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
