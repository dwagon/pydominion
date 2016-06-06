#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Salvager(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = """+1 Buy. Trash a card from your hand. Gain Coins equal to its cost."""
        self.name = 'Salvager'
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        card = player.plrTrashCard(force=True)
        player.output("Gained %d coin" % card[0].cost)
        player.addCoin(card[0].cost)


###############################################################################
class Test_Salvager(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Salvager'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Salvager'].remove()

    def test_play(self):
        """ Play a salvage """
        self.plr.setHand('Duchy', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertIsNotNone(self.g.inTrash('Duchy'))
        self.assertEqual(self.plr.getCoin(), 5)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
