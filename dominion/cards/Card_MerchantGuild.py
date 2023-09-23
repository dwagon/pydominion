#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles
from dominion.Counter import Counter


###############################################################################
class Card_MerchantGuild(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = """+1 Buy +1 Coin. While this is in play, when you buy a card, take a Coffer."""
        self.name = "Merchant Guild"
        self.coin = 1
        self.buys = 1
        self.cost = 5

    def hook_buy_card(self, game, player, card):
        player.output("Gaining Coin token from Merchant Guild")
        player.coffers.add(1)


###############################################################################
class TestMerchantGuild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Merchant Guild"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Merchant Guild")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy(self):
        """Play the card"""
        self.plr.coffers = Counter("C", 0)
        self.plr.play_card(self.card)
        self.plr.coins.set(3)
        self.plr.buy_card("Estate")
        self.assertEqual(self.plr.coffers.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
