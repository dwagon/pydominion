#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Guide(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = "+1 Card, +1 Action; Call to discard hand and draw 5"
        self.name = 'Guide'
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def hook_call_reserve(self, game, player):
        player.output("Discarding current hand and picking up 5 new cards")
        while player.hand:
            player.discardCard(player.hand.topcard())
        player.discardHand()
        player.pickupCards(5)


###############################################################################
class Test_Guide(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Guide'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Guide'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_call(self):
        """ Call Guide from reserve """
        self.plr.setHand('Estate', 'Estate')
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper')
        self.plr.setReserve('Guide')
        self.plr.call_reserve('Guide')
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discard_size(), 2)
        self.assertIsNone(self.plr.in_hand('Estate'))
        self.assertIsNotNone(self.plr.in_discard('Estate'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
