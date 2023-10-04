#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Prize_Goat"""
import unittest
from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_PrizeGoat(Loot.Loot):
    """PrizeGoat"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; +1 Buy; You may trash a card from your hand."
        self.name = "Prize Goat"
        self.purchasable = False
        self.coin = 3
        self.buys = 1
        self.cost = 7
        self.pile = "Loot"

    def special(self, game, player):
        """You may trash a card from your hand"""
        player.plr_trash_card(num=1)


###############################################################################
class Test_PrizeGoat(unittest.TestCase):
    """Test PrizeGoat"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_playing(self):
        """Test playing a prize goat"""
        goat = self.g.get_card_from_pile("Loot", "Prize Goat")
        self.plr.piles[Piles.HAND].set("Duchy", "Copper")
        self.plr.add_card(goat, Piles.HAND)
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.test_input = ["Trash Copper"]
        self.plr.play_card(goat)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
