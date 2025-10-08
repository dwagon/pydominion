#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Trader"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, OptionKeys, Player, NoCardException


###############################################################################
class Card_Trader(Card.Card):
    """Trader"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.
        When you would gain a card, you may reveal this from your hand. If you do, instead, gain a Silver."""
        self.name = "Trader"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if card := player.plr_trash_card(
            prompt="Trash a card from your hand. Gain a number of Silvers equal to its cost in coins."
        ):
            player.output(f"Gaining {card[0].cost} Silvers")
            for _ in range(card[0].cost):
                try:
                    player.gain_card("Silver")
                except NoCardException:
                    player.output("No more Silver")
                    break

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.name == "Silver":
            return {}
        if player.plr_choose_options(
            f"From your Trader gain {card} or gain a Silver instead?",
            (f"Still gain {card}", False),
            ("Instead gain Silver", True),
        ):
            return {OptionKeys.REPLACE: "Silver", OptionKeys.DESTINATION: Piles.DISCARD}
        return {}


###############################################################################
class TestTrader(unittest.TestCase):
    """Test Trader"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Trader"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Trader")

    def test_play(self) -> None:
        """Play a trader - trashing an estate"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["estate", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for i in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(i.name, "Silver")
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Estate", self.g.trash_pile)

    def test_gain(self) -> None:
        """Tet gain"""
        self.plr.test_input = ["Instead"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
