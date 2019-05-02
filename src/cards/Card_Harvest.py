#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Harvest(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = """Reveal the top 4 cards of your deck, then discard them. Coin per differently named card revealed."""
        self.name = 'Harvest'
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for i in range(4):
            c = player.nextCard()
            player.revealCard(c)
            cards.add(c.name)
            player.output("Revealed a %s" % c.name)
            player.addCard(c, 'discard')
        player.output("Gaining %d coins" % len(cards))
        player.addCoin(len(cards))


###############################################################################
class Test_Harvest(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Harvest'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Harvest'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Harvest """
        self.plr.setDeck('Duchy', 'Duchy', 'Silver', 'Copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Copper'))
        self.assertIsNone(self.plr.inDeck('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
