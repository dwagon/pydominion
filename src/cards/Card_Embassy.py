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
        player.plrDiscardCards(3, force=True)

    def hook_gainThisCard(self, game, player):
        """ When you gain this, each other player gains a Silver """
        for plr in game.playerList():
            if plr != player:
                plr.output("Gained a silver from %s's purchase of Embassy" % player.name)
                plr.gainCard('Silver')
        return {}


###############################################################################
class Test_Embassy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Embassy'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Embassy'].remove()
        self.plr.setDeck('Estate', 'Estate', 'Estate', 'Estate', 'Estate')
        self.plr.setHand('Copper', 'Silver', 'Gold', 'Estate', 'Duchy')
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.test_input = ['discard copper', 'discard silver', 'discard gold', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 5 - 3)

    def test_gain(self):
        self.plr.gainCard('Embassy')
        self.assertEqual(self.other.discardpile[-1].name, 'Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
