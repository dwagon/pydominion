#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Squire(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Coin. Choose one: +2 Actions; or +2 Buys; or gain a Silver.
        When you trash this, gain an Attack card."""
        self.name = "Squire"
        self.cost = 2
        self.coin = 1

    def special(self, game, player):
        choice = player.plrChooseOptions(
            "Choose one.",
            ("+2 Actions", "actions"),
            ("+2 Buys", "buys"),
            ("Gain a Silver", "silver"),
        )
        if choice == "actions":
            player.addActions(2)
        elif choice == "buys":
            player.add_buys(2)
        elif choice == "silver":
            player.gain_card("Silver")

    def hook_trashThisCard(self, game, player):
        attacks = []
        for cp in game.cardpiles.values():
            if cp.isAttack() and cp.purchasable:
                attacks.append(cp)
        cards = player.cardSel(prompt="Gain an attack card", cardsrc=attacks)
        player.gain_card(cards[0])


###############################################################################
class Test_Squire(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Squire", "Militia"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Squire"].remove()

    def test_play_actions(self):
        """Play a Squire - gain actions"""
        self.plr.test_input = [Card.TYPE_ACTION]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertIsNone(self.plr.in_discard("Silver"))

    def test_play_buys(self):
        """Play a Squire - gain buys"""
        self.plr.test_input = ["buys"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.get_buys(), 3)
        self.assertIsNone(self.plr.in_discard("Silver"))

    def test_play_silver(self):
        """Play a Squire - gain Silver"""
        self.plr.test_input = ["silver"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertIsNotNone(self.plr.in_discard("Silver"))

    def test_trash(self):
        """Trash a Squire"""
        self.plr.test_input = ["militia"]
        self.plr.trash_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Militia"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
