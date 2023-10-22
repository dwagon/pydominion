#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Figurehead"""
import unittest
from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_Figurehead(Loot.Loot):
    """Figurehead"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [
            Card.CardType.LOOT,
            Card.CardType.TREASURE,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; At the start of your next turn, +2 Cards."
        self.name = "Figurehead"
        self.coin = 3
        self.cost = 7
        self.pile = "Loot"

    def duration(self, game, player):
        """+2 cards"""
        player.pickup_cards(num=2)


###############################################################################
class Test_Figurehead(unittest.TestCase):
    """Test Figurehead"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = True
        while mods:
            mods = False
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Figurehead":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods = True

    def test_playing(self):
        """Test playing a figurehead"""
        figurehead = self.g.get_card_from_pile("Loot", "Figurehead")
        self.plr.add_card(figurehead, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(figurehead)
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_duration(self):
        """Test duration"""
        figurehead = self.g.get_card_from_pile("Loot", "Figurehead")
        self.plr.add_card(figurehead, Piles.HAND)
        self.plr.play_card(figurehead)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
