#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Crossroads(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action']
        self.base = 'hinterlands'
        self.desc = """Reveal your hand. +1 Card per Victory card revealed.
            If this is the first time you played a Crossroads this turn, +3 Actions."""
        self.name = 'Crossroads'
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        """ Reveal your hand. +1 Card per Victory card revealed.
            If this is the first time you played a Crossroads this turn,
            +3 Actions """
        vict = 0
        for card in player.hand:
            player.revealCard(card)
            if card.isVictory():
                vict += 1
        if vict:
            player.output("Picking up %d cards" % vict)
            player.pickupCards(vict)
        else:
            player.output("No victory cards")
        numcross = sum([1 for c in player.played if c.name == 'Crossroads'])
        if numcross == 1:
            player.addActions(3)


###############################################################################
class Test_Crossroads(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Crossroads'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Crossroads'].remove()

    def test_play(self):
        """ Play crossroads once"""
        self.plr.setHand('Silver', 'Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getActions(), 3)

    def test_play_twice(self):
        """ Play crossroads again """
        self.plr.setHand('Silver', 'Copper', 'Crossroads')
        self.plr.setPlayed('Crossroads')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertEqual(self.plr.getActions(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
