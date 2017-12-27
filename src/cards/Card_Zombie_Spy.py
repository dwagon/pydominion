#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Zombie_Spy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'zombie']
        self.base = 'nocturne'
        self.desc = "+1 Card; +1 Action; Look at the top card of your deck. Discard it or put it back."
        self.name = 'Zombie Spy'
        self.cost = 3
        self.insupply = False
        self.purchaseable = False
        self.numcards = 1
        self.cards = 1
        self.actions = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        c = player.nextCard()
        discard = player.plrChooseOptions(
            "Discard your card?",
            ("Keep %s on your deck" % c.name, False),
            ("Discard %s" % c.name, True))
        if discard:
            player.addCard(c, 'discard')
            player.output("Zombie Spy discarded your %s" % c.name)
        else:
            player.addCard(c, 'topdeck')


###############################################################################
class Test_Zombie_Spy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Zombie Spy'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Zombie Spy'].remove()

    def test_play_keep(self):
        self.plr.test_input = ['Keep']
        self.plr.setDeck('Province', 'Estate')
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertIsNotNone(self.plr.inDeck('Province'))

    def test_play_discard(self):
        self.plr.test_input = ['Discard']
        self.plr.setDeck('Province', 'Estate')
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertIsNone(self.plr.inDeck('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF