#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Doubloons"""
import unittest

from dominion import Loot, Card, Game, Piles, Player, OptionKeys


###############################################################################
class Loot_Doubloons(Loot.Loot):
    """Doubloons"""

    def __init__(self) -> None:
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; When you gain this, gain a Gold."
        self.name = "Doubloons"
        self.purchasable = False
        self.coin = 3
        self.cost = 7
        self.pile = "Loot"

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.gain_card("Gold")
        return {}


###############################################################################
class TestDoubloons(unittest.TestCase):
    """Test Doubloons"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Doubloons":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_gain_doubloon(self) -> None:
        """Test gaining doubloon"""
        self.g.assign_trait("Cursed", "Copper")
        self.plr.gain_card("Doubloons")
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_playing(self) -> None:
        """Test playing a doubloon"""
        doubloons = self.g.get_card_from_pile("Loot", "Doubloons")
        self.plr.add_card(doubloons, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(doubloons)
        self.assertEqual(self.plr.coins.get(), coins + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
