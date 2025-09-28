#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Poverty"""
import unittest

from dominion import Card, Game, Piles, Hex, Player


###############################################################################
class Hex_Poverty(Hex.Hex):
    """Poverty"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Discard down to 3 cards in hand"
        self.name = "Poverty"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Discard down to 3 cards in hand."""
        player.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    """Simple discard down to 3"""
    num_to_discard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Poverty(unittest.TestCase):
    """Test Poverty"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Poverty":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        """Test playing"""
        self.plr.test_input = ["1", "2", "0"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
