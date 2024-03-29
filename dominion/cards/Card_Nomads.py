#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Nomads"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Nomads(Card.Card):
    """Nomads"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = "+1 Buy; +$2; When you gain or trash this, +$2."
        self.coin = 2
        self.buys = 1
        self.name = "Nomads"
        self.cost = 4

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        """+$2"""
        player.coins.add(2)
        return {}

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        """+$2"""
        player.coins.add(2)
        return {}


###############################################################################
class Test_Nomads(unittest.TestCase):
    """Test Nomads"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Nomads"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Nomads")

    def test_play(self) -> None:
        """Play a card"""
        self.plr.add_card(self.card, Piles.HAND)
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 2)

    def test_gain(self) -> None:
        """Gain the card"""
        coins = self.plr.coins.get()
        self.plr.gain_card("Nomads")
        self.assertEqual(self.plr.coins.get(), coins + 2)

    def test_trash(self) -> None:
        """Trash the card"""
        coins = self.plr.coins.get()
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
