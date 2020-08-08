#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Wanderingminstrel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+1 Card, +2 Actions. Reveal the top 3 cards of your deck.
            Put the Actions back on top in any order and discard the rest."""
        self.name = 'Wandering Minstrel'
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        cards = []
        for _ in range(3):
            c = player.nextCard()
            player.revealCard(c)
            if c.isAction():
                cards.append(c)
                player.output("Revealed a %s and put on top of deck" % c.name)
            else:
                player.addCard(c, 'discard')
                player.output("Discarded %s" % c.name)

        for card in cards:
            player.addCard(card, 'topdeck')


###############################################################################
class Test_Wanderingminstrel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Wandering Minstrel', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Wandering Minstrel'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Wandering Minstrel """
        self.plr.setDeck('Duchy', 'Moat', 'Silver', 'Gold')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertIsNotNone(self.plr.in_deck('Moat'))
        self.assertIsNotNone(self.plr.in_discard('Duchy'))
        self.assertIsNotNone(self.plr.in_discard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
