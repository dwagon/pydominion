#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Panic"""
import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles


###############################################################################
class Prophecy_Panic(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "When you play a Treasure, +2 Buys, and when you discard one from play, return it to its pile."
        self.name = "Panic"

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        """When you play a Treasure, +2 Buys"""
        if card.isTreasure():
            player.buys.add(2)
        return {}

    def hook_discard_any_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        """when you discard one from play, return it to its pile."""
        if card.isTreasure():
            player.output(f"Discarding {card} due to Panic")
            player.move_card(card, Piles.CARDPILE)
        return {}


###############################################################################
class Test_Panic(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Panic"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play a Treasure"""
        buys = self.plr.buys.get()
        card = self.plr.gain_card("Gold")
        self.plr.play_card(card)
        self.assertEqual(self.plr.buys.get(), buys + 2)

    def test_discard(self) -> None:
        """Discard a Treasure"""
        num_gold = len(self.g.card_piles["Gold"])
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.gain_card("Gold", destination=Piles.HAND)
        self.plr.end_turn()
        self.g.print_state()
        self.assertEqual(len(self.g.card_piles["Gold"]), num_gold)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
