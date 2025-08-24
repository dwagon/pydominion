#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Herbalist"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, OptionKeys, Player


###############################################################################
class Card_Herbalist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = (
            "+1 buy, +1 coin. Once this turn, when you discard a Treasure from play, you may put it onto your deck."
        )
        self.name = "Herbalist"
        self.cost = 2
        self.buys = 1
        self.coin = 1

    def hook_discard_any_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        """Once this turn, when you discard a Treasure from play, you may put it onto your deck."""
        if not card.isTreasure():
            return {}
        if player.do_once(self.uuid):
            if player.plr_choose_options(
                "Herbalist lets you put treasures on top of deck",
                (f"Discard {card} as normal", False),
                (f"Put {card} onto your deck", True),
            ):
                player.move_card(card, Piles.TOPDECK)
        return {}


###############################################################################
class Test_Herbalist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Herbalist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.herbalist = self.g.get_card_from_pile("Herbalist")

    def test_keep_nothing(self):
        self.plr.piles[Piles.PLAYED].set("Gold", "Estate")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.herbalist, Piles.HAND)
        self.plr.play_card(self.herbalist)
        self.plr.test_input = ["Discard Gold"]
        self.plr.discard_hand()
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_put_gold(self):
        self.plr.piles[Piles.PLAYED].set("Gold", "Estate")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.herbalist, Piles.HAND)
        self.plr.play_card(self.herbalist)
        self.plr.test_input = ["onto your deck"]
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
