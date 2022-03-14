#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_SpiceMerchant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """You may trash a Treasure from your hand. If you do, choose one: +2 Cards and +1 Action; or +2 Coins and +1 Buy."""
        self.name = "Spice Merchant"
        self.cost = 4

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        tr = player.plr_trash_card(
            prompt="Trash a treasure from your hand for +2 Cards, +1 Action / +2 Coins, +1 Buy",
            cardsrc=treasures,
        )
        if tr:
            rew = player.plrChooseOptions(
                "Select your reward",
                ("+2 Cards, +1 Action", "cards"),
                ("+2 Coins, +1 Buy", "coins"),
            )
            if rew == "cards":
                player.pickup_cards(2)
                player.add_actions(1)
            else:
                player.add_coins(2)
                player.add_buys(1)


###############################################################################
class Test_SpiceMerchant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Spice Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Spice Merchant"].remove()

    def test_play_card(self):
        """Play an Spice Merchant and select cards"""
        tsize = self.g.trashSize()
        self.plr.set_hand("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Gold", "cards"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_coins(), 0)

    def test_play_coins(self):
        """Play an Spice Merchant and select coins"""
        tsize = self.g.trashSize()
        self.plr.set_hand("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Gold", "coins"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_coins(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
