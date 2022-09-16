#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Winemerchant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Buy, +4 Coin, Put this on your Tavern mat; At the
            end of your Buy phase, if you have at least 2 Coin unspent, you
            may discard this from your Tavern mat."""
        self.name = "Wine Merchant"
        self.buys = 1
        self.coin = 4
        self.cost = 5
        self.callable = False

    def hook_cleanup(self, game, player):
        if player.coin >= 2:
            player.output("Discarding Wine Merchant")
            player.reserve.remove(self)
            player.add_card(self, "discard")


###############################################################################
class Test_Winemerchant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wine Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Wine Merchant"].remove()
        self.card.player = self.plr

    def test_play(self):
        """Play a Wine Merchant"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 4)

    def test_recover(self):
        """Recover a wine merchant"""
        self.plr.coin = 2
        self.plr.reserve.set("Wine Merchant")
        for crd in self.plr.reserve:
            crd.player = self.plr
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.turn()
        self.assertEqual(self.plr.reserve.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
