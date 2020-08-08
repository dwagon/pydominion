#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_CityQuarter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = "+2 Actions. Reveal your hand. +1 Card per Action card revealed."
        self.name = 'City Quarter'
        self.debtcost = 8
        self.actions = 2
        self.coin = 1

    def special(self, game, player):
        actions = 0
        for c in player.hand:
            player.revealCard(c)
            if c.isAction():
                actions += 1
        player.output("Revealed %d actions" % actions)
        player.pickupCards(actions)


###############################################################################
class Test_CityQuarter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['City Quarter', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['City Quarter'].remove()

    def test_play(self):
        """ Play a City Quarter """
        self.plr.setHand('Moat', 'Moat', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.handSize(), 3 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
