#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Doubloons"""
import unittest
from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_Doubloons(Loot.Loot):
    """Doubloons"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = Card.CardType.LOOT
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; When you gain this, gain a Gold."
        self.name = "Doubloons"
        self.purchasable = False
        self.coin = 3
        self.cost = 7
        self.pile = "Loot"

    def hook_gain_this_card(self, game, player):
        player.gain_card("Gold")


###############################################################################
class Test_Doubloons(unittest.TestCase):
    """Test Doubloons"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gain_doubloon(self):
        """Test gaining doubloon"""
        self.g.assign_trait("Cursed", "Copper")
        self.plr.gain_card("Doubloons")
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_playing(self):
        """Test playing a doubloon"""
        doubloon = self.plr.gain_card("Doubloons")
        self.plr.move_card(doubloon, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(doubloon)
        self.assertEqual(self.plr.coins.get(), coins + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
