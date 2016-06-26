#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Soothsayer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'guilds'
        self.desc = "Gain a Gold. Each other player gains a Curse. Each player who did draws a card."
        self.required_cards = ['Curse']
        self.name = 'Soothsayer'
        self.cost = 5

    def special(self, game, player):
        player.output("Gained up a Gold")
        player.gainCard('Gold')
        for pl in player.attackVictims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's Soothsayer cursed you" % player.name)
            pl.gainCard('Curse')
            pl.pickupCard()


###############################################################################
class Test_Soothsayer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Soothsayer'])
        self.g.startGame()
        self.attacker, self.victim = self.g.playerList()
        self.wcard = self.g['Soothsayer'].remove()
        self.attacker.addCard(self.wcard, 'hand')

    def test_play(self):
        self.attacker.playCard(self.wcard)
        self.assertEqual(self.victim.handSize(), 6)
        self.assertIsNotNone(self.victim.inDiscard('Curse'))
        self.assertIsNotNone(self.attacker.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF