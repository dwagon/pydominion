#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Fortune"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Fortune(Card.Card):
    """Fortune"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+1 Buy; Double your $ if you haven't yet this turn.
            When you gain this, gain a Gold per Gladiator you have in play."""
        self.name = "Fortune"
        self.cost = 8
        self.debtcost = 8
        self.buys = 1
        self.numcards = 5
        self.pile = "Gladiator"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.do_once("Fortune"):
            coins = player.coins.get()
            player.output(f"Gained {coins} coins to double money")
            player.coins.add(coins)

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        num_cards = sum(1 for _ in player.piles[Piles.HAND] if _.name == "Gladiator")
        for _ in range(num_cards):
            player.gain_card("Gold")
        return {}


###############################################################################
class TestFortune(unittest.TestCase):
    """Test Fortune"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Gladiator"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Gladiator", "Fortune")

    def test_gain(self) -> None:
        """Gain a Fortune"""
        self.plr.piles[Piles.HAND].set("Silver", "Copper", "Gladiator")
        self.plr.gain_card(new_card=self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_play(self) -> None:
        """Spend a fortune"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coins.set(3)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
