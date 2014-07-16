#!/usr/bin/env python

import unittest
from Card import Card


class Card_Scout(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 action, Adjust top 4 cards of deck"
        self.name = 'Scout'
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Reveal the top 4 cards of your deck. Put the revealed
            victory cards into your hand. Put the other cards on top
            of your deck in any order """
        #TODO: Currently you can't order the cards you return
        cards = []
        for i in range(4):
            c = player.nextCard()
            if c.isVictory():
                player.addCard(c, 'hand')
                player.output("Adding %s to hand" % c.name)
            else:
                cards.append(c)
        for c in cards:
            player.output("Putting %s back on deck" % c.name)
            player.addCard(c, 'deck')


###############################################################################
class Test_Scout(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['scout'])
        self.plr = self.g.playerList(0)
        self.scout = self.g['scout'].remove()

    def test_play(self):
        self.plr.addCard(self.scout, 'hand')
        self.plr.playCard(self.scout)
        self.assertEqual(self.plr.getActions(), 1)

    def test_victory(self):
        self.plr.setHand()
        self.plr.addCard(self.scout, 'hand')
        self.plr.playCard(self.scout)
        for c in self.plr.hand:
            self.assertTrue(c.isVictory())

    def test_deck(self):
        self.plr.setHand()
        self.plr.addCard(self.scout, 'hand')
        self.plr.setDeck('copper', 'copper', 'copper', 'duchy')
        self.plr.playCard(self.scout)
        self.assertEqual(self.plr.hand[0].name, 'Duchy')
        for c in self.plr.deck:
            self.assertEqual(c.name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
