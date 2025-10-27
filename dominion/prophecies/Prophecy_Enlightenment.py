#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Enlightenment"""
import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, Phase, Piles
from dominion.Card import CardType


###############################################################################
class Prophecy_Enlightenment(Prophecy.Prophecy):
    """Enlightenment"""

    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Treasures are also Actions. When you play a Treasure in an Action phase,
            instead of following its instructions, +1 Card and +1 Action."""
        self.name = "Enlightenment"

    def hook_pre_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if card.isTreasure() and player.phase == Phase.ACTION:
            player.output(f"Enlightenment acting instead of {card}")
            player.pickup_cards(1)
            player.actions.add(1)
            return {OptionKeys.SKIP_CARD: True}
        return {}

    def hook_add_dynamic_card_type(self, card: "Card.Card") -> CardType:
        """Treasures are also Actions."""
        if Card.CardType.TREASURE in card.get_raw_card_type():
            return Card.CardType.ACTION
        return Card.CardType.UNDEFINED


###############################################################################
class TestEnlightenment(unittest.TestCase):
    """Test Enlightenment"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Enlightenment"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_treasure(self) -> None:
        """Treasures are also Actions."""
        self.plr.test_input = ["Get Duchy"]
        gold = self.plr.get_card_from_pile("Gold")
        self.assertTrue(gold.isAction())

    def test_play(self) -> None:
        """Play a Treasure in an Action Phase"""
        self.plr.phase = Phase.ACTION
        gold = self.plr.get_card_from_pile("Gold")
        coins = self.plr.coins.get()
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(gold)
        self.assertEqual(self.plr.coins.get(), coins)
        self.assertEqual(self.plr.actions.get(), actions)  # +1 for card, -1 for playing it
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)

    def test_play_treasure_buy(self) -> None:
        """Play a Treasure in a Buy Phase"""
        self.plr.phase = Phase.BUY
        gold = self.plr.get_card_from_pile("Gold")
        coins = self.plr.coins.get()
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(gold)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertEqual(self.plr.actions.get(), actions)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
