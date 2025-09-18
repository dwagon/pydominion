#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_WineMerchant(Card.Card):
    """Wine Merchant"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Buy, +4 Coin, Put this on your Tavern mat; At the
            end of your Buy phase, if you have at least 2 Coin unspent, you
            may discard this from your Tavern mat."""
        self.name = "Wine Merchant"
        self.buys = 1
        self.coin = 4
        self.cost = 5
        self.callable = False

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """At the end of your Buy phase, if you have at least 2 Coin unspent, you
        may discard this from your Tavern mat."""
        # Merchant might not be in RESERVE if, for example, intercepted by Enchantress
        if player.coins.get() >= 2 and self in player.piles[Piles.RESERVE]:
            player.output(f"Discarding {self}")
            player.piles[Piles.RESERVE].remove(self)
            player.add_card(self, Piles.DISCARD)
        return {}


###############################################################################
class TestWineMerchant(unittest.TestCase):
    """Test Wine Merchant"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wine Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wine Merchant")
        self.card.player = self.plr

    def test_play(self) -> None:
        """Play a Wine Merchant"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 4)

    def test_recover(self) -> None:
        """Recover a wine merchant"""
        self.plr.coins.set(2)
        self.plr.piles[Piles.RESERVE].set("Wine Merchant")
        for crd in self.plr.piles[Piles.RESERVE]:
            crd.player = self.plr
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.do_turn()
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
