#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Dismantle(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'promo'
        self.desc = "Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold."
        self.name = 'Dismantle'
        self.cost = 4

    def special(self, game, player):
        tc = player.plrTrashCard(
            force=True, printcost=True,
            prompt="Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold."
        )
        cost = tc[0].cost
        if cost:
            player.plrGainCard(cost=cost-1)
            player.output("Gained a Gold")
            player.gainCard('Gold')


###############################################################################
class Test_Dismantle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Dismantle'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.rcard = self.g['Dismantle'].remove()

    def test_free(self):
        self.plr.setHand('Copper', 'Estate', 'Silver', 'Province')
        self.plr.addCard(self.rcard, 'hand')
        self.plr.test_input = ['trash copper']
        self.plr.playCard(self.rcard)
        self.assertIsNotNone(self.g.in_trash('Copper'))
        self.assertEqual(self.plr.discard_size(), 0)
        self.assertEqual(self.plr.handSize(), 3)

    def test_non_free(self):
        self.plr.setHand('Estate', 'Silver', 'Province')
        self.plr.addCard(self.rcard, 'hand')
        self.plr.test_input = ['trash estate', 'get copper']
        self.plr.playCard(self.rcard)
        self.assertIsNotNone(self.g.in_trash('Estate'))
        self.assertEqual(self.plr.discard_size(), 2)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertIsNotNone(self.plr.in_discard('Copper'))
        self.assertEqual(self.plr.handSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
