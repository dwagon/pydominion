#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_SpiceMerchant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """You may trash a Treasure from your hand. If you do, choose one: +2 Cards and +1 Action; or +2 Coins and +1 Buy."""
        self.name = "Spice Merchant"
        self.cost = 4

    def special(self, game, player):
        treasures = [c for c in player.piles[Piles.HAND] if c.isTreasure()]
        tr = player.plr_trash_card(
            prompt="Trash a treasure from your hand for +2 Cards, +1 Action / +2 Coins, +1 Buy",
            cardsrc=treasures,
        )
        if tr:
            rew = player.plr_choose_options(
                "Select your reward",
                ("+2 Cards, +1 Action", "cards"),
                ("+2 Coins, +1 Buy", "coins"),
            )
            if rew == "cards":
                player.pickup_cards(2)
                player.add_actions(1)
            else:
                player.coins.add(2)
                player.buys.add(1)


###############################################################################
class Test_SpiceMerchant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Spice Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Spice Merchant")

    def test_play_card(self):
        """Play an Spice Merchant and select cards"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold", "cards"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_play_coins(self):
        """Play an Spice Merchant and select coins"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold", "coins"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
