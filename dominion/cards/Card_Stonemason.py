#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_StoneMason(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.name = "Stonemason"
        self.overpay = True
        self.cost = 2

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """Trash a card from your hand. Gain 2 cards each costing less
                than it.  When you buy this, you may overpay for it. If you do,
                gain 2 Actions each costing the amount you overpaid."""
        return "Trash a card from your hand. Gain 2 cards each costing less than it."

    def special(self, game, player):
        tc = player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain 2 cards each costing less than it.",
        )
        if tc:
            cost = player.card_cost(tc[0]) - 1
            if cost < 0:
                player.output("No suitable cards")
                return
            for _ in range(2):
                player.plr_gain_card(cost, "less")

    def hook_overpay(self, game, player, amount):
        if amount:
            player.plr_gain_card(
                amount,
                "less",
                types={Card.CardType.ACTION: True},
                prompt="Gain a card costing up to %s" % amount,
            )
            player.plr_gain_card(
                amount,
                "less",
                types={Card.CardType.ACTION: True},
                prompt="Gain another card costing up to %s" % amount,
            )


###############################################################################
class TestStoneMason(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Stonemason", "Moat"],
            badcards=["Fool's Gold"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Stonemason"].remove()

    def test_play(self):
        """Play a stonemason"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash province", "get gold", "get silver"]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trashpile)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_buy(self):
        self.plr.coins.set(5)
        self.plr.test_input = ["3", "Moat", "Stonemason"]
        self.plr.buy_card(self.g["Stonemason"])
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Stonemason", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
