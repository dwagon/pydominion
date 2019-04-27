#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Priest(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.name = 'Priest'
        self.desc = "+2 Coin. Trash a card from your hand. For the rest of this turn, when you trash a card, +2 Coin."
        self.cost = 4
        self.coin = 2
        self.in_special = False

    ###########################################################################
    def special(self, game, player):
        self.in_special = True
        player.plrTrashCard(force=True)
        self.in_special = False

    ###########################################################################
    def hook_trashCard(self, game, player, card):
        if not self.in_special:
            player.output("Adding 2 from Priest")
            player.addCoin(2)


###############################################################################
class Test_Priest(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Priest', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Priest'].remove()
        self.plr.addCard(self.card, 'hand')
        self.moat = self.g['Moat'].remove()
        self.plr.addCard(self.moat, 'hand')
        self.gold = self.g['Gold'].remove()
        self.plr.addCard(self.gold, 'hand')

    def test_playCard(self):
        self.plr.test_input = ['Trash Moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.g.inTrash('Moat'))
        self.plr.trashCard(self.gold)
        self.assertEqual(self.plr.getCoin(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
