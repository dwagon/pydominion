#!/usr/bin/env python

import unittest
from Card import Card


class Card_Seahag(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'seaside'
        self.desc = "Curse everyone else"
        self.needcurse = True
        self.name = 'Sea Hag'
        self.cost = 4

    def special(self, game, player):
        """ Each other player discards the top card of his deck,
            then gains a Curse card, putting it on top of his deck"""
        for pl in player.attackVictims():
            c = pl.nextCard()
            pl.discardCard(c)
            pl.output("Discarded your %s" % c.name)
            pl.gainCard('curse', destination='topdeck')
            pl.output("Got cursed by %s's Sea Hag" % player.name)
            player.output("%s got cursed" % pl.name)


###############################################################################
class Test_Seahag(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['seahag', 'moat'])
        self.attacker = self.g.players[0]
        self.victim = self.g.players[1]
        self.seahag = self.g['seahag'].remove()
        self.mcard = self.g['moat'].remove()
        self.attacker.addCard(self.seahag, 'hand')

    def test_defended(self):
        self.victim.addCard(self.mcard, 'hand')
        self.attacker.playCard(self.seahag)
        self.assertEqual(len(self.victim.hand), 6)
        self.assertNotEqual(self.victim.deck[0].name, 'Curse')
        self.assertEqual(self.victim.discardpile, [])

    def test_nodefense(self):
        self.victim.setDeck('gold')
        self.attacker.playCard(self.seahag)
        self.assertEqual(len(self.victim.hand), 5)
        self.assertEqual(self.victim.discardpile[0].name, 'Gold')
        self.assertEqual(self.victim.deck[0].name, 'Curse')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
