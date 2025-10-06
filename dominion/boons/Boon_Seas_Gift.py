#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/The_Sea%27s_Gift"""
import unittest

from dominion import Boon, Card, Game, Piles


###############################################################################
class Boon_Seas_Gift(Boon.Boon):
    """Sea's Gift"""

    def __init__(self) -> None:
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Card"
        self.name = "The Sea's Gift"
        self.purchasable = False
        self.cards = 1


###############################################################################
class TestSeasGift(unittest.TestCase):
    """Test Sea's Gift"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Sea's Gift":
                self.g.boons = [b]
                break
        self.card = self.g.get_card_from_pile("Bard")

    def test_seas_gift(self) -> None:
        """Teest boon"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
