#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Cutpurse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.desc = "+2 coin; Each other player discards a Copper card (or reveals a hand with no Copper)."
        self.name = 'Cutpurse'
        self.coin = 2
        self.cost = 4
        self.base = 'seaside'

    def special(self, game, player):
        """ Each other player discard a Copper card (or reveals a
            hand with no copper)."""
        for victim in player.attackVictims():
            c = victim.in_hand('Copper')
            if c:
                player.output("%s discarded a copper" % victim.name)
                victim.output("Discarded a copper due to %s's Cutpurse" % player.name)
                victim.discardCard(c)
            else:
                for card in victim.hand:
                    victim.revealCard(card)
                player.output("%s had no coppers" % victim.name)


###############################################################################
class Test_Cutpurse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Cutpurse'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Cutpurse'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_coppers(self):
        self.victim.setHand('Copper', 'Copper', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile[-1].name, 'Copper')
        self.assertEqual(self.victim.handSize(), 2)

    def test_play_none(self):
        self.victim.setHand('Estate', 'Estate', 'Estate')
        self.plr.playCard(self.card)
        self.assertTrue(self.victim.discardpile.is_empty())
        self.assertEqual(self.victim.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
