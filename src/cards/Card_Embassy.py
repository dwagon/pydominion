#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Embassy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+5 Cards, Discard 3. Everyone gets a silver on purchase"
        self.name = 'Embassy'
        self.cost = 5
        self.cards = 5

    def special(self, game, player):
        player.plrDiscardCards(3)

    def hook_gainThisCard(self, game, player):
        """ When you gain this, each other player gains a Silver """
        for plr in game.players:
            if plr != player:
                plr.output("Gained a silver from %s's purchase of Embassy" % player.name)
                plr.gainCard('Silver')


###############################################################################
class Test_Embassy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['embassy'])
        self.plr = self.g.players[0]
        self.other = self.g.players[1]
        self.card = self.g['embassy'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.test_input = ['1', '2', '3', '0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 5 + 5 - 3)

    def test_gain(self):
        self.plr.gainCard('embassy')
        self.assertEqual(self.other.discardpile[-1].name, 'Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
