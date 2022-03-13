#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_SilkMerchant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """+2 Cards; +1 Buy; When you gain or trash this, +1 Coffers and +1 Villager."""
        self.name = "Silk Merchant"
        self.cards = 2
        self.cost = 4

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.add_villager()
        player.add_coffer()

    ###########################################################################
    def hook_trashThisCard(self, game, player):
        player.add_villager()
        player.add_coffer()


###############################################################################
class Test_SilkMerchant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Silk Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Silk Merchant"].remove()
        self.plr.set_hand()

    def test_gain_card(self):
        self.plr.setCoffer(0)
        self.plr.gainCard("Silk Merchant")
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertEqual(self.plr.getVillager(), 1)
        self.assertEqual(self.plr.getCoffer(), 1)

    def test_trash_card(self):
        self.plr.setCoffer(0)
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertEqual(self.plr.getVillager(), 1)
        self.assertEqual(self.plr.getCoffer(), 1)

    def test_play_card(self):
        self.plr.add_card(self.card, "hand")
        self.plr.setCoffer(0)
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.getCoffer(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
