#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Envy"""
import unittest

from dominion import Card, Game, Hex, Player


###############################################################################
class Hex_Envy(Hex.Hex):
    """Envy"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "If you don't have Deluded or Envious, take Envious."
        self.name = "Envy"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """If you don't have Deluded or Envious, take Envious."""
        if player.has_state("Deluded") or player.has_state("Envious"):
            return
        player.assign_state("Envious")


###############################################################################
class Test_Envy(unittest.TestCase):
    """Tet Envy"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Envy":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_preexisting(self):
        """We are deluded"""
        self.plr.assign_state("Deluded")
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Deluded"))

    def test_normal(self):
        """Not deluded"""
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Envious"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
