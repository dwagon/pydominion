#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Haggler"""
import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Haggler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+2 Coin. 
        While this is in play, when you buy a card, gain a card costing less than it that is not a Victory card."""
        self.name = "Haggler"
        self.coin = 2
        self.cost = 5

    def hook_buy_card(self, game, player, card):
        cost = card.cost - 1
        player.plr_gain_card(
            cost=cost,
            types={Card.CardType.ACTION: True, Card.CardType.TREASURE: True},
            prompt=f"Gain a non-Victory card costing under {cost}",
        )


###############################################################################
class Test_Haggler(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Haggler"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Haggler"].remove()

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_buy(self):
        """Buy a Gold and haggle a silver"""
        self.plr.piles[Piles.PLAYED].set("Haggler")
        self.plr.test_input = ["Get Silver"]
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
