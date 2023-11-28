#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Piles, Game, Card, Player, NoCardException, OptionKeys, Phase


###############################################################################
class Card_Cache(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.HINTERLANDS
        self.name = "Cache"
        self.cost = 5
        self.coin = 3

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+3 coin. Gain two coppers when you gain this"
        return "+3 coin"

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, Any]]:
        """When you gain this, gain two Coppers"""
        player.output("Gained 2 copper from cache")
        for _ in range(2):
            try:
                player.gain_card("Copper")
            except NoCardException:
                player.output("No more Copper")
                break
        return {}


###############################################################################
class Test_Cache(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Cache"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.cache = self.g.get_card_from_pile("Cache")

    def test_gain(self) -> None:
        self.plr.gain_card("Cache")
        sdp = sorted([c.name for c in self.plr.piles[Piles.DISCARD]])
        self.assertEqual(sorted(["Copper", "Copper", "Cache"]), sdp)

    def test_play(self) -> None:
        self.plr.add_card(self.cache, Piles.HAND)
        self.plr.play_card(self.cache)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
