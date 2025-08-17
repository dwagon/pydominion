#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Wish"""
import unittest

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Wish(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Action; Return this to its pile. If you did, gain a card to your hand costing up to 6."
        self.name = "Wish"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cost = 0
        self.numcards = 12

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if self.location != Piles.PLAYED:
            player.output("Already returned to pile")
            return
        if player.plr_choose_options(
            "Return this to gain a card to your hand costing up to 6",
            ("Return", True),
            ("Keep", False),
        ):
            game.card_piles["Wish"].add(self)
            player.piles[Piles.PLAYED].remove(self)
            self.location = None
            player.plr_gain_card(cost=6)


###############################################################################
class TestWish(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wish", "Daimyo"], badcards=["Gold Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wish")

    def test_return(self) -> None:
        num_wishes = len(self.g.card_piles["Wish"])
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Return", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Wish", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Wish", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.g.card_piles["Wish"]), num_wishes + 1)

    def test_keep(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Wish", self.plr.piles[Piles.PLAYED])

    def test_play_twice(self) -> None:
        """Play the same Wish twice"""
        num_wishes = len(self.g.card_piles["Wish"])
        self.plr.piles[Piles.PLAYED].set("Daimyo")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Return", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Wish", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Wish", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.g.card_piles["Wish"]), num_wishes + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
