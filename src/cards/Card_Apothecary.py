#!/usr/bin/env python

import unittest
from Card import Card


class Card_Apothecary(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+1 card, +1 action, Take coppers and potions out of top 4 of deck"
        self.name = 'Apothecary'
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.potcost = 1

    def special(self, player, game):
        """ Reveal the top 4 cards of your deck. Put the revealed
            Coppers and Potions into your hand. Put the other cards
            back on top of your deck in any order """
        unput = []
        for i in range(4):
            c = player.nextCard()
            if c.name in ('Copper', 'Potion'):
                player.output("Putting %s in hand" % c.name)
                player.addCard(c, 'hand')
            else:
                unput.append(c)
        for c in unput:
            player.output("Putting %s back in deck" % c.name)
            player.addCard(c, 'deck')


###############################################################################
class Test_Apothecary(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['apothecary'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_none(self):
        self.plr.setHand('apothecary')
        apoth = self.plr.hand[0]
        self.plr.setDeck('duchy', 'estate', 'estate', 'estate', 'province')
        self.plr.playCard(apoth)
        self.assertEqual(self.plr.handSize(), 1)  # P
        self.assertEqual(self.plr.deckSize(), 4)  # D + E + E + E

    def test_some(self):
        self.plr.setHand('apothecary')
        apoth = self.plr.hand[0]
        self.plr.setDeck('duchy', 'potion', 'copper', 'estate', 'province')
        self.plr.playCard(apoth)
        self.assertEqual(self.plr.handSize(), 3)  # P + C + Pot
        self.assertEqual(self.plr.deckSize(), 2)  # E + D


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
