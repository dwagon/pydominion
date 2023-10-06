#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Dismantle(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROMO
        self.desc = "Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold."
        self.name = "Dismantle"
        self.cost = 4

    def special(self, game, player):
        tc = player.plr_trash_card(
            force=True,
            printcost=True,
            prompt="Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold.",
        )
        cost = tc[0].cost
        if cost:
            player.plr_gain_card(cost=cost - 1)
            player.gain_card("Gold")


###############################################################################
class Test_Dismantle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Dismantle"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.rcard = self.g.get_card_from_pile("Dismantle")

    def test_free(self):
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Silver", "Province")
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rcard)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)

    def test_non_free(self):
        self.plr.piles[Piles.HAND].set("Estate", "Silver", "Province")
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["trash estate", "get copper"]
        self.plr.play_card(self.rcard)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
