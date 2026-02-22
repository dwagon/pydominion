#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Jewelled_Egg"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_JewelledEgg(Card.Card):
    """Jewelled Egg"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$1; +1 Buy; When you trash this, gain a Loot."
        self.name = "Jewelled Egg"
        self.required_cards = ["Loot"]
        self.cost = 2
        self.coin = 1
        self.buys = 1

    def hook_trash_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        player.gain_card("Loot")
        return {}


###############################################################################
class TestJewelledEgg(unittest.TestCase):
    """Test Jewelled Egg"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Jewelled Egg"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Jewelled Egg")

    def test_play(self) -> None:
        """Play a Jewelled Egg"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)

    def test_trash(self) -> None:
        """Trash the card"""
        self.plr.piles[Piles.DISCARD].empty()
        self.plr.trash_card(self.card)
        self.assertIn("Jewelled Egg", self.g.trash_pile)
        found = any(True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot())
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
