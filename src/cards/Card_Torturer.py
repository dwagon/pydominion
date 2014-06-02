#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Torturer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = "+3 cards; Other players discard 2 cards or gain a curse"
        self.needcurse = True
        self.name = 'Torturer'
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        """ Each other player chooses one: he discards 2 cards; or
            he gains a Curse card, putting it in his hand """
        for plr in player.attackVictims():
            plr.output("Choose:")
            self.choiceOfDoom(plr, player)

    def choiceOfDoom(self, victim, player):
        victim.output("Your hand is: %s" % ", ".join([c.name for c in victim.hand]))
        options = [
            {'selector': '0', 'print': 'Discard 2 cards', 'choice': 'discard'},
            {'selector': '1', 'print': 'Gain a curse card', 'choice': 'curse'}
        ]
        o = victim.userInput(options, "Discard or curse")
        if o['choice'] == 'discard':
            player.output("%s discarded" % victim.name)
            victim.plrDiscardCards(2)
        else:
            player.output("%s opted for a curse" % victim.name)
            victim.gainCard('curse', 'hand')


###############################################################################
class Test_Torturer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['torturer', 'moat'])
        self.plr = self.g.players[0]
        self.victim = self.g.players[1]
        self.card = self.g['torturer'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_opt_curse(self):
        """ Play the torturer - victim opts for a curse"""
        self.victim.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 8)
        self.assertTrue(self.victim.inHand('Curse'))

    def test_opt_discard(self):
        """ Play the torturer - victim opts for discarding"""
        self.victim.test_input = ['0', '1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 8)
        self.assertEqual(len(self.victim.hand), 3)
        self.assertFalse(self.victim.inHand('Curse'))

    def test_defended(self):
        """ Defending against a torturer """
        self.victim.setHand('moat')
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 8)
        self.assertEqual(len(self.victim.hand), 1)
        self.assertFalse(self.victim.inHand('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
