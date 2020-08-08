#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Smugglers(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.SEASIDE
        self.desc = """Gain a copy of a card costing up to 6 that the player to your right gained on his last turn."""
        self.name = 'Smugglers'
        self.cost = 3

    def special(self, game, player):
        plr = game.playerToRight(player)
        cards = [c for c in plr.stats['bought'] if c.cost <= 6]
        if cards:
            card = player.cardSel(cardsrc=cards)
            if card:
                player.addCard(card[0])
        else:
            player.output("%s didn't buy any suitable cards" % plr.name)


###############################################################################
class Test_Smugglers(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Smugglers'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g['Smugglers'].remove()

    def test_play(self):
        """ Play a smugglers"""
        self.other.stats['bought'] = [self.g['Gold'].remove()]
        self.plr.test_input = ['gold']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
