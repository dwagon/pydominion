#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Endless_Chalice"""
import unittest
from typing import Optional

from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_EndlessChalice(Loot.Loot):
    """Endless Chalice"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [
            Card.CardType.LOOT,
            Card.CardType.TREASURE,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Now and at the start of each of your turns for the rest of the game: $1; +1 Buy"
        self.name = "Endless Chalice"
        self.coin = 1
        self.buys = 1
        self.cost = 7
        self.pile = "Loot"
        self.permanent = True

    def duration(self, game, player) -> Optional[dict]:
        player.coins.add(1)
        player.buys.add(1)


###############################################################################
class TestEndlessChalice(unittest.TestCase):
    """Test Endless Chalice"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_playing(self):
        """Test playing an Endless Chalice"""
        chalice = self.g.get_card_from_pile("Loot", "Endless Chalice")
        self.plr.add_card(chalice, Piles.HAND)
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.play_card(chalice)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.g.print_state()
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
