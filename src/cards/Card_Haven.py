#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Haven(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = Game.SEASIDE
        self.desc = "+1 cards, +1 action; play a card next turn"
        self.name = 'Haven'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Set aside a card from your hand face down. At the start of
            your next turn, put it into your hand. """
        c = player.plrPickCard(force=True, prompt='Pick card to put into hand next turn')
        player.addCard(c, 'duration')
        player.hand.remove(c)
        self.savedHavenCard = c

    def duration(self, game, player):
        c = self.savedHavenCard
        player.addCard(c, 'hand')
        # Can't guarantee the order so it may be in played
        # or still in durationpile
        if c in player.played:
            player.played.remove(c)
        elif c in player.durationpile:
            player.durationpile.remove(c)
        player.output("Pulling %s out of from haven" % c)
        del self.savedHavenCard


###############################################################################
class Test_Haven(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Haven'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Haven'].remove()
        self.plr.setDiscard('Copper', 'Copper', 'Copper', 'Copper', 'Copper')
        self.plr.setDeck('Estate', 'Estate', 'Estate', 'Estate', 'Gold')
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a haven """
        self.plr.test_input = ['select gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.durationSize(), 2)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.played_size(), 1)
        self.assertTrue(self.plr.in_hand('Gold'))
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
