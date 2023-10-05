#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Sword"""
import unittest
from dominion import Loot, Card, Game, Piles


###############################################################################
class Loot_Sword(Loot.Loot):
    """Sword"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; +1 Buy; Each other player discards down to 4 cards in hand."
        self.name = "Sword"
        self.coin = 3
        self.cost = 7
        self.buys = 1
        self.pile = "Loot"

    def special(self, game, player):
        """Each other player discards down to 4 cards in hand."""
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Sword: Discard down to 4 cards")
            plr.plr_discard_down_to(4)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    num_to_discard = len(player.piles[Piles.HAND]) - 4
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Sword(unittest.TestCase):
    """Test Sword"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, traits=["Cursed"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Sword":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self):
        """Test playing a doubloon"""
        sword = self.g.get_card_from_pile("Loot", "Sword")
        self.plr.add_card(sword, Piles.HAND)
        coins = self.plr.coins.get()
        self.victim.test_input = ["1", "0"]
        self.plr.play_card(sword)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertEqual(len(self.victim.piles[Piles.HAND]), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
