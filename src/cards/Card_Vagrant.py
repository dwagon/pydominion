#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Vagrant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = """+1 card, +1 action, Reveal the top card of your deck.
        If it's a Curse, Ruins, Shelter or Victory card, put it into your hand"""
        self.name = 'Vagrant'
        self.actions = 1
        self.cards = 1
        self.cost = 2

    def special(self, game, player):
        """" Reveal the top card of your deck. If it's a Curse,
            Ruins, Shelter or Victory card, put it into your hand """
        c = player.nextCard()
        if c.isVictory() or c.isRuin() or c.isShelter() or c.name == 'Ruins':
            player.addCard(c, 'hand')
            player.output("Adding %s to hand" % c.name)
        else:
            player.addCard(c, 'topdeck')
            player.output("Top card %s still on deck" % c.name)


###############################################################################
class Test_Vagrant(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Vagrant'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Vagrant'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the vagrant with unexciting next card"""
        self.plr.setDeck('Gold', 'Silver', 'Copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.nextCard().name, 'Silver')

    def test_play_exciting(self):
        """ Play the vagrant with an exciting next card"""
        self.plr.setDeck('Estate', 'Province', 'Duchy')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertTrue(self.plr.inHand('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
