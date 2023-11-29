#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Embassy(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.desc = "+5 Cards, Discard 3. Everyone gets a silver on purchase"
        self.name = "Embassy"
        self.cost = 5
        self.base = Card.CardExpansion.HINTERLANDS
        self.cards = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.plr_discard_cards(3, force=True)

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, Any]]:
        """When you gain this, each other player gains a Silver"""
        for plr in game.player_list():
            if plr != player:
                try:
                    plr.gain_card("Silver")
                    plr.output(f"Gained a silver from {player}'s purchase of Embassy")
                except NoCardException:
                    player.output("No more Silver")
                    plr.output("No more Silver")
        return {}


###############################################################################
class Test_Embassy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Embassy"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Embassy")
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate", "Estate", "Estate")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.test_input = [
            "discard copper",
            "discard silver",
            "discard gold",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 5 - 3)

    def test_gain(self) -> None:
        self.plr.gain_card("Embassy")
        self.assertEqual(self.other.piles[Piles.DISCARD][-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
