#!/usr/bin/env python

import unittest
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

    def special(self, game, player):
        cards = []
        for i in range(5):
            c = player.nextCard()
            cards.append(c)
        player.output("Top 5 cards on the deck are: %s" % ", ".join([c.name for c in cards]))
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

    def hook_gainThisCard(self, game, player):
        return {'destination': 'hand'}


###############################################################################
class Test_NightWatchman(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Night Watchman'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Night Watchman'].remove()

    def test_play(self):
        self.plr.setDeck('Gold', 'Province', 'Gold', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Return Silver', 'Discard Duchy', 'Return Gold', 'Discard Province', 'Return Gold']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertIsNone(self.plr.inDiscard('Gold'))
        self.assertIsNone(self.plr.inDiscard('Silver'))

        self.assertIsNone(self.plr.inDeck('Duchy'))
        self.assertIsNone(self.plr.inDeck('Province'))
        self.assertIsNotNone(self.plr.inDeck('Gold'))
        self.assertIsNotNone(self.plr.inDeck('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF