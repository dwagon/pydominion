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
        ans = player.plrChooseOptions(
            'What to do with the alchemist?',
            ('Discard alchemist', False), ('Put on top of deck', True))
        if ans:
            player.played.remove(self)
            player.addCard(self, 'topdeck')


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['alchemist'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.alchemist = self.g['alchemist'].remove()
        self.plr.addCard(self.alchemist, 'hand')

    def test_play(self):
        self.plr.playCard(self.alchemist)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 7)

    def test_nopotion(self):
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(self.plr.discardSize(), 8)  # 5 for hand, +2 cards, alch

    def test_discard(self):
        self.plr.setPlayed('potion')
        self.plr.test_input = ['discard']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(self.plr.discardSize(), 9)  # 5 for hand, +2 cards, alch, pot
        for c in self.plr.discardpile:
            if c.name == 'Alchemist':
                break
        else:   # pragma: no cover
            self.fail()

    def test_keep(self):
        self.plr.setPlayed('potion')
        self.plr.test_input = ['top of deck']
        self.plr.playCard(self.alchemist)
        self.plr.discardHand()
        self.assertEqual(self.plr.discardSize(), 8)  # 5 for hand, +2 cards, pot
        for c in self.plr.discardpile:
            if c.name == 'Alchemist':   # pragma: no cover
                self.fail()
        self.assertEquals(self.plr.deck[-1].name, 'Alchemist')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
