#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_Miser(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Put a copper onto your mat or +1 coin per copper on mat"
        self.name = "Miser"
        self.cost = 4

    def special(self, game, player):
        """Choose one: Put a Copper from your hand onto your Tavern mat;
        or +1 Coin per Copper on your Tavern mat."""
        inhand = sum([1 for _ in player.piles[Piles.HAND] if _.name == "Copper"])
        coins = sum([1 for _ in player.piles[Piles.RESERVE] if _.name == "Copper"])
        deposit = False
        if inhand:
            deposit = player.plr_choose_options(
                "Which to do?",
                ("Put a copper onto tavern mat?", True),
                ("%d coins from mat" % coins, False),
            )
            if deposit:
                cu = player.piles[Piles.HAND]["Copper"]
                player.add_card(cu, Piles.RESERVE)
                player.piles[Piles.HAND].remove(cu)
        if not deposit:
            player.output("Adding %d coins from tavern" % coins)
            player.coins.add(coins)


###############################################################################
class Test_Miser(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Miser"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Miser")

    def test_put(self):
        """Play a miser with coppers in hand"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["put"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.RESERVE]["Copper"])
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])

    def test_put_none(self):
        """Play a miser with no coppers in hand"""
        self.plr.piles[Piles.HAND].set("Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.piles[Piles.RESERVE]["Copper"])
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 0)

    def test_add(self):
        """Play a miser with coppers in reserve"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.piles[Piles.RESERVE].set("Copper", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["coins from mat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 2)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
