#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_NightWatchman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night']
        self.base = 'nocturne'
        self.desc = "Look at the top 5 cards of your deck, discard any number, and put the rest back in any order."
        self.name = 'Night Watchman'
        self.cost = 3

    def night(self, game, player):
        cards = []
        for _ in range(5):
            c = player.nextCard()
            cards.append(c)
        player.output("Top 5 cards on the deck are: %s" % ", ".join([_.name for _ in cards]))
        for c in cards:
            discard = player.plrChooseOptions(
                'What do you want to do?',
                ('Discard {}'.format(c.name), True),
                ('Return {} to the deck'.format(c.name), False)
                )
            if discard:
                player.discardCard(c)
            else:
                player.addCard(c, 'topdeck')

    def hook_gain_this_card(self, game, player):
        return {'destination': 'hand'}


###############################################################################
class Test_NightWatchman(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Night Watchman'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Night Watchman'].remove()

    def test_play(self):
        self.plr.phase = 'night'
        self.plr.setDeck('Gold', 'Province', 'Gold', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Return Silver', 'Discard Duchy', 'Return Gold', 'Discard Province', 'Return Gold']
        self.plr.playCard(self.card)
        try:
            self.assertIsNotNone(self.plr.inDiscard('Duchy'))
            self.assertIsNotNone(self.plr.inDiscard('Province'))
            self.assertIsNone(self.plr.inDiscard('Gold'))
            self.assertIsNone(self.plr.inDiscard('Silver'))

            self.assertIsNone(self.plr.in_deck('Duchy'))
            self.assertIsNone(self.plr.in_deck('Province'))
            self.assertIsNotNone(self.plr.in_deck('Gold'))
            self.assertIsNotNone(self.plr.in_deck('Silver'))
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
