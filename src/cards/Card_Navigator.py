#!/usr/bin/env python

import unittest
from Card import Card


class Card_Navigator(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = "+2 gold. Discard top 5 cards, or put them back on deck"
        self.name = 'Navigator'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Look at the top 5 cards of your deck. Either discard
            all of them, or put them back on top of your deck in any
            order """
        cards = []
        for i in range(5):
            cards.append(player.nextCard())
        player.output("Top 5 cards on the deck are: %s" % ", ".join([c.name for c in cards]))
        discard = player.plrChooseOptions(
            'What do you want to do?',
            ('Discard cards', True), ('Return them to the deck', False))
        if discard:
            for c in cards:
                player.discardCard(c)
        else:
            # TODO - let player choose order
            for c in cards:
                player.addCard(c, 'topdeck')


###############################################################################
class Test_Navigator(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['navigator'])
        self.plr = self.g.players.values()[0]
        self.navigator = self.g['navigator'].remove()
        self.plr.addCard(self.navigator, 'hand')

    def test_discard(self):
        self.plr.setDeck('copper', 'estate', 'gold', 'province', 'silver', 'duchy')
        self.plr.test_input = ['0']
        self.plr.playCard(self.navigator)
        self.assertEqual(len(self.plr.discardpile), 5)
        self.assertEqual(len(self.plr.deck), 1)

    def test_keep(self):
        self.plr.setDeck('copper', 'estate', 'gold', 'province', 'silver', 'duchy')
        self.plr.test_input = ['1']
        self.plr.playCard(self.navigator)
        self.assertEqual(len(self.plr.discardpile), 0)
        self.assertEqual(len(self.plr.deck), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
