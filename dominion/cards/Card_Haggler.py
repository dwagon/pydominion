#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Haggler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = "+2 Coin. While this is in play, when you buy a card, gain a card costing less than it that is not a Victory card."
        self.name = "Haggler"
        self.coin = 2
        self.cost = 5

    def hook_buy_card(self, game, player, card):
        cost = card.cost - 1
        player.plrGainCard(
            cost=cost,
            types={Card.TYPE_ACTION: True, Card.TYPE_TREASURE: True},
            prompt="Gain a non-Victory card costing under %s" % cost,
        )


###############################################################################
class Test_Haggler(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Haggler"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Haggler"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_buy(self):
        """Buy a Gold and haggle a silver"""
        self.plr.set_played("Haggler")
        self.plr.test_input = ["Get Silver"]
        self.plr.setCoin(6)
        self.plr.buyCard(self.g["Gold"])
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
