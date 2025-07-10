#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Hammer"""
import unittest

from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_Hammer(Loot.Loot):
    """Hammer"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; Gain a card costing up to $4."
        self.name = "Hammer"
        self.coin = 3
        self.cost = 7
        self.pile = "Loot"

    def special(self, game, player):
        """Gain a card costing up to $4"""
        player.plr_gain_card(4)


###############################################################################
class Test_Hammer(unittest.TestCase):
    """Test Hammer"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Hammer":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self):
        """Test playing a doubloon"""
        hammer = self.g.get_card_from_pile("Loot", "Hammer")
        self.plr.add_card(hammer, Piles.HAND)
        self.plr.test_input = ["Get Silver"]
        coins = self.plr.coins.get()
        self.plr.play_card(hammer)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
