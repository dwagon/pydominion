#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Witch(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "+2 cards; Each other player gains a Curse card."
        self.required_cards = ['Curse']
        self.name = 'Witch'
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """ All other players gain a curse """
        for pl in player.attackVictims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's witch cursed you" % player.name)
            pl.gainCard('Curse')


###############################################################################
class Test_Witch(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Witch', 'Moat'])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.wcard = self.g['Witch'].remove()
        self.mcard = self.g['Moat'].remove()
        self.attacker.addCard(self.wcard, 'hand')

    def test_defended(self):
        self.victim.addCard(self.mcard, 'hand')
        self.attacker.playCard(self.wcard)
        self.assertEqual(self.victim.handSize(), 6)
        self.assertEqual(self.attacker.handSize(), 7)
        self.assertEqual(self.victim.discardSize(), 0)

    def test_nodefense(self):
        self.attacker.playCard(self.wcard)
        self.assertEqual(self.victim.handSize(), 5)
        self.assertEqual(self.attacker.handSize(), 7)
        self.assertEqual(self.victim.discardpile[0].name, 'Curse')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
