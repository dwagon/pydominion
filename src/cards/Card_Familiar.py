#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Familiar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'alchemy'
        self.desc = "+1 card, +1 action; Each other player gains a Curse."
        self.name = 'Familiar'
        self.cards = 1
        self.actions = 1
        self.cost = 3
        self.required_cards = ['Potion', 'Curse']
        self.potcost = True

    def special(self, game, player):
        """ All other players gain a curse """
        for pl in player.attackVictims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's Familiar cursed you" % player.name)
            pl.gainCard('Curse')


###############################################################################
class Test_Familiar(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Familiar', 'Moat'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Familiar'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a familiar """
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile[0].name, 'Curse')
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)

    def test_defended(self):
        self.victim.setHand('Gold', 'Moat')
        self.plr.playCard(self.card)
        self.assertTrue(self.victim.discardpile.is_empty())
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
