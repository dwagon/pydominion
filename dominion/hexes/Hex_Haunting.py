#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Haunting"""
import unittest

from dominion import Card, Game, Piles, Hex, Player


###############################################################################
class Hex_Haunting(Hex.Hex):
    """Haunting"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "If you have at least 4 cards in hand, put one of them onto your deck."
        self.name = "Haunting"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """If you have at least 4 cards in hand, put one of them onto your deck."""
        if player.piles[Piles.HAND].size() >= 4:
            card = player.card_sel(force=True)
            player.add_card(card[0], Piles.TOPDECK)
            player.piles[Piles.HAND].remove(card[0])


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    """Just discard one"""
    return player.pick_to_discard(1)


###############################################################################
class Test_Haunting(unittest.TestCase):
    """Test Haunting"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Haunting":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_none(self):
        """Not really a test - but don't have at least four cards"""
        self.plr.piles[Piles.HAND].set("Duchy", "Gold", "Silver")
        self.plr.gain_card("Cursed Village")

    def test_activate(self):
        """Have four cards"""
        self.plr.piles[Piles.HAND].set("Duchy", "Gold", "Silver", "Province")
        self.plr.test_input = ["Gold"]
        self.plr.gain_card("Cursed Village")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
