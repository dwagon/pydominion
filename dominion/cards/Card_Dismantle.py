#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Dismantle(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROMO
        self.desc = "Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold."
        self.name = "Dismantle"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        trash_cards = player.plr_trash_card(
            force=True,
            printcost=True,
            prompt="Trash a card from your hand. If it costs 1 or more, gain a cheaper card and a Gold.",
        )
        if not trash_cards or trash_cards[0] is None:
            return
        cost = trash_cards[0].cost
        if cost:
            player.plr_gain_card(cost=cost - 1)
            player.gain_card("Gold")


###############################################################################
class TestDismantle(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Dismantle"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.rcard = self.g.get_card_from_pile("Dismantle")

    def test_free(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Silver", "Province")
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rcard)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)

    def test_non_free(self) -> None:
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
