#!/usr/bin/env python

import unittest
from Card import Card


class Card_Alchemist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+2 cards, +1 action; can put on top of deck if potion in play"
        self.name = 'Alchemist'
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = 1

    def hook_discardCard(self, game, player):
        """ When you discard this from play, you may put this on
            top of your deck if you have a Potion in play """
        for c in player.played:
            if c.name == 'Potion':
                break
        else:
            return
        options = [
            {'selector': '0', 'print': 'Discard', 'todeck': False},
            {'selector': '1', 'print': 'Put on top of deck', 'todeck': True},
        ]
        o = player.userInput(options, 'What to do with the alchemist?')
        if o['todeck']:
            player.played.remove(self)
            player.addCard(self, 'topdeck')


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['alchemist'])
        self.plr = self.g.players[0]
        self.alchemist = self.g['alchemist'].remove()
        self.plr.addCard(self.alchemist, 'hand')

    def test_play(self):
        self.plr.playCard(self.alchemist)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(len(self.plr.hand), 7)

    def test_nopotion(self):
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(len(self.plr.discardpile), 8)  # 5 for hand, +2 cards, alch

    def test_discard(self):
        self.plr.setPlayed('potion')
        self.plr.test_input = ['0']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(len(self.plr.discardpile), 9)  # 5 for hand, +2 cards, alch, pot
        for c in self.plr.discardpile:
            if c.name == 'Alchemist':
                break
        else:
            self.fail()

    def test_keep(self):
        self.plr.setPlayed('potion')
        self.plr.test_input = ['1']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(len(self.plr.discardpile), 8)  # 5 for hand, +2 cards, pot
        for c in self.plr.discardpile:
            if c.name == 'Alchemist':
                self.fail()
        self.assertEquals(self.plr.deck[-1].name, 'Alchemist')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
