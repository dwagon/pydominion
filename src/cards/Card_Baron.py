#!/usr/bin/env python

import unittest
from Card import Card


class Card_Baron(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 Buy, discard an estate gain +4 Gold, else gain estate"
        self.name = 'Baron'
        self.cost = 4
        self.buys = 1

    def special(self, game, player):
        """ You may discard an Estate card. If you do +4 GP. Otherwise,
            gain an estate card """
        hasEstate = player.inHand('Estate')
        if hasEstate:
            options = [
                {'selector': '0', 'print': "Keep Estate - Gain another", 'discard': False},
                {'selector': '1', 'print': "Discard an Estate - Gain +4 Gold", 'discard': True}]
            o = player.userInput(options, "Discard Estate?")
            if o['discard']:
                player.discardCard(hasEstate)
                player.t['gold'] += 4
                return
        player.output("Gained an Estate")
        player.gainCard('estate')


###############################################################################
class Test_Baron(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['baron'])
        self.plr = self.g.players.values()[0]
        self.baron = self.g['baron'].remove()

    def test_play(self):
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.t['buys'], 2)

    def test_noestate(self):
        self.plr.setHand('copper', 'copper', 'copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(len(self.plr.discardpile), 1)

    def test_discardestate(self):
        self.plr.setHand('gold', 'estate', 'copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.t['gold'], 4)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(self.plr.inHand('Estate'), None)

    def test_keepestate(self):
        self.plr.setHand('estate', 'gold', 'copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertNotEqual(self.plr.inHand('Estate'), None)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
