#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_SilkMerchant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = """+2 Cards; +1 Buy; When you gain or trash this, +1 Coffers and +1 Villager."""
        self.name = 'Silk Merchant'
        self.cards = 2
        self.cost = 4

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        player.gainVillager()
        player.gainCoffer()

    ###########################################################################
    def hook_trashThisCard(self, game, player):
        player.gainVillager()
        player.gainCoffer()


###############################################################################
class Test_SilkMerchant(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Silk Merchant'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Silk Merchant'].remove()
        self.plr.setHand()

    def test_gain_card(self):
        self.plr.setCoffer(0)
        self.plr.gainCard('Silk Merchant')
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.getVillager(), 1)
        self.assertEqual(self.plr.getCoffer(), 1)

    def test_trash_card(self):
        self.plr.setCoffer(0)
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.getVillager(), 1)
        self.assertEqual(self.plr.getCoffer(), 1)

    def test_play_card(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.setCoffer(0)
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.getCoffer(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
