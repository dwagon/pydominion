#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Familiar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'alchemy'
        self.desc = "+1 card, +1 action, curse everyone else"
        self.needcurse = True
        self.name = 'Familiar'
        self.cards = 1
        self.actions = 1
        self.cost = 3
        self.potcost = 1

    def special(self, game, player):
        """ All other players gain a curse """
        for pl in player.attackVictims():
            player.output("%s got cursed" % pl.name)
            pl.gainCard('curse')


###############################################################################
class Test_Familiar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['familiar', 'moat'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['familiar'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a familiar """
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile[0].name, 'Curse')
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)

    def test_defended(self):
        self.victim.setHand('gold', 'moat')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile, [])
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
