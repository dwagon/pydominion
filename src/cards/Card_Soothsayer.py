#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Soothsayer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.GUILDS
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
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Soothsayer'])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.wcard = self.g['Soothsayer'].remove()
        self.attacker.addCard(self.wcard, 'hand')

    def test_play(self):
        self.attacker.playCard(self.wcard)
        self.assertEqual(self.victim.handSize(), 6)
        self.assertIsNotNone(self.victim.in_discard('Curse'))
        self.assertIsNotNone(self.attacker.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
