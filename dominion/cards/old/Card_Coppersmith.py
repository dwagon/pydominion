#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_Coppersmith(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "Copper produces an extra +1 this turn"
        self.name = "Coppersmith"
        self.cost = 4

    def hook_spend_value(self, game, player, card):
        """Copper produces an extra 1 this turn"""
        if card.name == "Copper":
            player.output("Copper worth 1 more")
            return 1
        return 0


###############################################################################
class Test_Coppersmith(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Coppersmith"], oldcards=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Coppersmith")

    def test_copper(self):
        """Copper should be worth two"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.play_card(self.plr.piles[Piles.HAND][0])
        self.assertEqual(self.plr.coins.get(), 2)

    def test_silver(self):
        """Silver should be unchanged and worth two"""
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.play_card(self.plr.piles[Piles.HAND][0])
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
