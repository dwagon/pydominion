#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Navigator(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.SEASIDE
        self.desc = """+2 coin. Look at the top 5 cards of your deck.
            Either discard all of them, or put them back on top of your deck
            in any order"""
        self.name = 'Navigator'
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        cards = []
        for _ in range(5):
            cards.append(player.nextCard())
        player.output("Top 5 cards on the deck are: %s" % ", ".join([c.name for c in cards]))
        discard = player.plrChooseOptions(
            'What do you want to do?',
            ('Discard cards', True), ('Return them to the deck', False))
        if discard:
            for c in cards:
                player.discardCard(c)
        else:
            for c in cards:
                player.addCard(c, 'topdeck')


###############################################################################
class Test_Navigator(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Navigator'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.navigator = self.g['Navigator'].remove()
        self.plr.addCard(self.navigator, 'hand')

    def test_discard(self):
        self.plr.setDeck('Copper', 'Estate', 'Gold', 'Province', 'Silver', 'Duchy')
        self.plr.test_input = ['discard']
        self.plr.playCard(self.navigator)
        self.assertEqual(self.plr.discard_size(), 5)
        self.assertEqual(self.plr.deckSize(), 1)

    def test_keep(self):
        self.plr.setDeck('Copper', 'Estate', 'Gold', 'Province', 'Silver', 'Duchy')
        self.plr.test_input = ['return']
        self.plr.playCard(self.navigator)
        self.assertEqual(self.plr.discard_size(), 0)
        self.assertEqual(self.plr.deckSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
