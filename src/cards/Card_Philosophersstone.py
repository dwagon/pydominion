#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Philosophersstone(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'alchemy'
        self.desc = "Gain +1 Gold for every 5 cards in deck + discard"
        self.name = "Philosopher's Stone"
        self.cost = 3
        self.potcost = 1

    def hook_goldvalue(self, game, player):
        """ When you play this, count your deck and discard pile.
            Worth 1 per 5 cards total between them (rounded down) """
        numcards = len(player.deck) + len(player.discardpile)
        extragold = numcards / 5
        return extragold


###############################################################################
class Test_Philosophersstone(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['philosophersstone'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['philosophersstone'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a philosophers stone with not much on"""
        self.plr.setDeck('estate')
        self.plr.setDiscard('estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 0)

    def test_play_value(self):
        """ Play a philosophers stone with the full Nicholas Flamel """
        self.plr.setDeck('estate', 'estate', 'estate', 'estate', 'silver')
        self.plr.setDiscard('estate', 'estate', 'estate', 'estate', 'silver')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
