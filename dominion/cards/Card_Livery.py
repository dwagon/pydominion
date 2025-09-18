#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Livery"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, OptionKeys, Player


###############################################################################
class Card_Livery(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+3 Coins; This turn, when you gain a card costing 4 Coins or more, gain a Horse."""
        self.name = "Livery"
        self.coin = 3
        self.cost = 5
        self.required_cards = [("Card", "Horse")]

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        for card in player.stats["gained"]:
            if card.cost > 4:
                player.output("Gained a Horse from Livery")
                player.gain_card("Horse")
        return {}


###############################################################################
class Test_Livery(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Livery"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Livery")
        self.card.player = self.plr
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard_cost0(self) -> None:
        """Play a livery and gain something worth 0"""
        self.plr.play_card(self.card)
        self.plr.gain_card("Copper")
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.do_turn()
        self.assertNotIn("Horse", self.plr.piles[Piles.DISCARD])

    def test_playcard_cost6(self) -> None:
        """Play a livery and gain something worth 6"""
        self.plr.play_card(self.card)
        self.plr.gain_card("Province")
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.do_turn()
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
