#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Hex


###############################################################################
class Hex_Misery(Hex.Hex):
    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "If this is your first Misery this game, take Miserable. Otherwise, flip it over to Twice Miserable."
        self.name = "Misery"
        self.purchasable = False

    def special(self, game, player):
        if player.has_state("Twice Miserable"):
            pass
        elif player.has_state("Miserable"):
            player.remove_state("Miserable")
            player.assign_state("Twice Miserable")
        else:
            player.assign_state("Miserable")


###############################################################################
class Test_Misery(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Misery":
                self.g.hexes.remove(h)

    def test_normal(self):
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Miserable"))
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Twice Miserable"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
