#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Misery"""
import unittest

from dominion import Card, Game, Hex, Player


###############################################################################
class Hex_Misery(Hex.Hex):
    """Misery"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """If this is your first Misery this game, take Miserable.
                Otherwise, flip it over to Twice Miserable."""
        self.name = "Misery"
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """If this is your first Misery this game, take Miserable. Otherwise, flip it over to Twice Miserable."""
        if player.has_state("Twice Miserable"):
            pass
        elif player.has_state("Miserable"):
            player.remove_state("Miserable")
            player.assign_state("Twice Miserable")
        else:
            player.assign_state("Miserable")


###############################################################################
class Test_Misery(unittest.TestCase):
    """Test Misery"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for h in self.g.hexes[:]:
            if h.name != "Misery":
                self.g.hexes.remove(h)

    def test_play(self):
        """Test normal play"""
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Miserable"))
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Twice Miserable"))
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Twice Miserable"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
